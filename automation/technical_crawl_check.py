#!/usr/bin/env python3
"""
Read-only technical SEO crawl check. Never modifies site/ — only reads it and
writes findings to reports/technical_crawl/. Checks:
  - basic HTML validity (unclosed tags via html.parser, best-effort)
  - broken internal links (hrefs to local paths that don't resolve to a file)
  - duplicate <title> tags across pages
  - sitemap.xml validity (parses, counts URLs, flags URLs not present on disk)
"""

import json
import logging
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler('logs/technical_crawl.log'), logging.StreamHandler()],
)
logger = logging.getLogger('technical_crawl')

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
             "meta", "param", "source", "track", "wbr"}


class BalanceChecker(HTMLParser):
    """Best-effort unclosed-tag detector. Not a full validator."""
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass  # self-closed, fine

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"unexpected closing </{tag}> with nothing open")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            # mismatched nesting — pop until we find it
            self.errors.append(f"mismatched nesting: expected </{self.stack[-1]}>, got </{tag}>")
            while self.stack and self.stack[-1] != tag:
                self.stack.pop()
            if self.stack:
                self.stack.pop()

    def unclosed(self):
        return self.stack


def check_html_validity(site_dir: Path):
    logger.info("Checking HTML validity (unclosed/mismatched tags)...")
    issues = []
    for f in site_dir.rglob("*.html"):
        text = f.read_text(encoding="utf-8", errors="replace")
        parser = BalanceChecker()
        try:
            parser.feed(text)
        except Exception as e:
            issues.append({"file": str(f), "error": f"parse exception: {e}"})
            continue
        unclosed = parser.unclosed()
        if unclosed:
            issues.append({"file": str(f), "unclosed_tags": unclosed, "count": len(unclosed)})
        if parser.errors:
            issues.append({"file": str(f), "mismatch_errors": parser.errors[:5]})
    logger.info(f"HTML validity: {len(issues)} files with issues")
    return issues


def check_broken_internal_links(site_dir: Path):
    logger.info("Checking internal links resolve to real files...")
    href_re = re.compile(r'href="(/[^"]*)"')
    broken = defaultdict(list)
    checked = 0
    for f in site_dir.rglob("*.html"):
        text = f.read_text(encoding="utf-8", errors="replace")
        for href in href_re.findall(text):
            checked += 1
            path = href.split("#")[0].split("?")[0]
            if not path or path == "/":
                continue
            candidate = site_dir / path.lstrip("/")
            resolved = candidate if candidate.suffix else (candidate / "index.html")
            if candidate.suffix == "" and not resolved.exists():
                if not candidate.exists():
                    broken[str(f)].append(href)
            elif candidate.suffix and not candidate.exists():
                broken[str(f)].append(href)
    logger.info(f"Checked {checked} internal hrefs; {sum(len(v) for v in broken.values())} broken across {len(broken)} files")
    return dict(broken)


def check_duplicate_titles(site_dir: Path):
    logger.info("Checking for duplicate <title> tags...")
    title_re = re.compile(r'<title>([^<]*)</title>')
    by_title = defaultdict(list)
    for f in site_dir.rglob("*.html"):
        text = f.read_text(encoding="utf-8", errors="replace")
        m = title_re.search(text)
        if m:
            by_title[m.group(1).strip()].append(str(f))
    dupes = {t: files for t, files in by_title.items() if len(files) > 1}
    logger.info(f"Duplicate titles: {len(dupes)} titles shared by {sum(len(v) for v in dupes.values())} pages")
    return dupes


def check_hreflang_canonical(site_dir: Path):
    """Checks reciprocal hreflang and presence of a canonical tag on localized homepage variants."""
    logger.info("Checking hreflang reciprocity and canonicals...")
    lang_home_dirs = {"es", "de", "fr", "nl", "no", "pl", "ru", "sv", "ar", "uk"}
    hreflang_re = re.compile(r'<link rel="alternate" hreflang="([a-zA-Z-]+)" href="([^"]+)"')
    canonical_re = re.compile(r'<link rel="canonical" href="([^"]+)"')

    pages = {}
    for code in lang_home_dirs | {"en"}:
        f = site_dir / code / "index.html" if code != "en" else site_dir / "index.html"
        if f.exists():
            pages[code] = f

    issues = []
    declared = {}
    for code, f in pages.items():
        text = f.read_text(encoding="utf-8", errors="replace")
        tags = hreflang_re.findall(text)
        canon = canonical_re.search(text)
        declared[code] = {h: href for h, href in tags}
        if not canon:
            issues.append({"page": str(f), "issue": "missing canonical tag"})

    for code, alts in declared.items():
        for target_lang, target_href in alts.items():
            if target_lang == "x-default":
                continue
            if target_lang not in declared:
                continue  # target page doesn't exist on disk, not a reciprocity issue we can check
            back = declared[target_lang]
            # does the target page point back to `code`?
            points_back = any(k == code or k == ("en" if code == "en" else code) for k in back)
            if not points_back:
                issues.append({
                    "page": code, "issue": f"hreflang to '{target_lang}' not reciprocated back to '{code}'",
                })

    logger.info(f"hreflang/canonical: {len(issues)} issues across {len(pages)} language homepages checked")
    return {"pages_checked": list(pages.keys()), "issues": issues}


def check_sitemap(site_dir: Path):
    logger.info("Checking sitemap.xml validity...")
    sitemap_path = site_dir / "sitemap.xml"
    result = {"exists": sitemap_path.exists()}
    if not result["exists"]:
        logger.warning("No sitemap.xml found at site/sitemap.xml")
        return result
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [loc.text for loc in root.findall(".//sm:loc", ns)]
        result["valid_xml"] = True
        result["url_count"] = len(urls)
        missing_on_disk = []
        for u in urls[:2000]:
            path = urlparse(u).path
            candidate = site_dir / path.lstrip("/")
            if not candidate.exists() and not (candidate / "index.html").exists():
                missing_on_disk.append(u)
        result["urls_missing_on_disk"] = missing_on_disk[:50]
        result["urls_missing_count"] = len(missing_on_disk)
        logger.info(f"Sitemap: {len(urls)} URLs, {len(missing_on_disk)} not found on disk")
    except ET.ParseError as e:
        result["valid_xml"] = False
        result["error"] = str(e)
        logger.error(f"Sitemap XML parse error: {e}")
    return result


def run():
    root = Path(__file__).parent.parent
    site_dir = root / "site"
    out_dir = root / "reports" / "technical_crawl"
    out_dir.mkdir(parents=True, exist_ok=True)

    from datetime import datetime
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "html_validity_issues": check_html_validity(site_dir),
        "broken_internal_links": check_broken_internal_links(site_dir),
        "duplicate_titles": check_duplicate_titles(site_dir),
        "hreflang_canonical": check_hreflang_canonical(site_dir),
        "sitemap": check_sitemap(site_dir),
    }

    date = datetime.utcnow().date().isoformat()
    out_file = out_dir / f"crawl_report_{date}.json"
    out_file.write_text(json.dumps(report, indent=2))
    logger.info(f"Report saved: {out_file}")

    total_issues = (
        len(report["html_validity_issues"])
        + len(report["broken_internal_links"])
        + len(report["duplicate_titles"])
    )
    logger.info(f"TOTAL ISSUES FOUND: {total_issues}")
    return report


if __name__ == "__main__":
    run()
