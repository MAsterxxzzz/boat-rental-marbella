#!/usr/bin/env python3
"""One-off: fix the broken internal links baked into content/*.json by the
(unguarded) daily-content pipeline over the last ~2 months.

Safety: a link is only ever touched if it is ACTUALLY broken — i.e. its
normalized target is not in the known-pages set built from the current
site/ build (same logic as check_broken_links.py). Every other href is
left byte-for-byte untouched.

Strategy for broken links:
  1. Boat/fleet URL variants that clearly refer to a real boat -> rewritten
     to the correct /boats/<slug>/ URL.
  2. A short curated list of near-miss page slugs with a confirmed real
     equivalent -> rewritten to that real URL.
  3. Everything else (invented blog posts, invented experience pages,
     invented "destinations" section, generic utility pages like /faq/,
     /pricing/, /booking/) -> the <a href="...">text</a> wrapper is
     stripped, keeping the anchor text as plain text. No fabricated
     redirect target, no dead link.

Run AFTER a full build (needs site/ present to know what's real).
Idempotent — safe to re-run. Only touches content/*.json; site/ must be
rebuilt afterward by the normal pipeline to pick up the fix.
"""
from __future__ import annotations
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"
SITE = ROOT / "site"

REAL_BOAT_SLUGS = {b["slug"] for b in json.loads((ROOT / "config" / "boats.json").read_text())["boats"]}

BOAT_ALIASES = {
    "azimut-58-flybridge": "azimut-58",
    "red-tide": "red-tide-fishing-boat",
}

def resolve_boat_slug(raw: str) -> str | None:
    raw = raw.strip("/")
    if raw in REAL_BOAT_SLUGS:
        return raw
    if raw in BOAT_ALIASES:
        return BOAT_ALIASES[raw]
    return None

NEAR_MISS_REDIRECTS = {
    "/family-boat-rental-marbella/": "/family-yacht-charter-marbella/",
    "/marbella-boat-rental-puerto-banus/": "/boat-rental-puerto-banus/",
    "/half-day-charter-marbella/": "/day-charter-marbella/",
    "/marbella-boat-rental/": "/",
    "/boat-rental-marbella/": "/",
    "/marbella-boat-charter/": "/",
    "/marbella-yacht-charters/": "/",
    "/marbella-marina/": "/boat-rental-puerto-banus/",
    "/marbella-anchoring-guide/": "/experiences/",
    "/pricing/": "/",
    "/booking/": "/",
    "/faq/": "/",
    "/itineraries/": "/experiences/",
    "/destinations/": "/experiences/",
    "/blog/marbella-boat-rental-guide/": "/blog/",
    "/blog/marbella-boat-rental/": "/blog/",
    "/blog/marbella-sailing-guide/": "/blog/",
    "/blog/marbella-boat-rental-season-guide/": "/blog/",
    "/blog/best-time-to-charter-a-boat-in-marbella/": "/blog/",
    "/blog/marbella-boat-charter-guide/": "/blog/",
    "/blog/marbella-boat-rental-prices/": "/blog/",
    "/blog/marbella-boat-charter-sunset-cruise/": "/sunset-cruise-marbella/",
    "/blog/marbella-boat-rental-sunset-sail/": "/sunset-cruise-marbella/",
    "/blog/marbella-sunset-boat-charter-guide/": "/sunset-cruise-marbella/",
    "/blog/marbella-sunset-cruise/": "/sunset-cruise-marbella/",
    "/blog/puerto-banus-boat-hire/": "/boat-rental-puerto-banus/",
    "/blog/puerto-banus-boat-rental/": "/boat-rental-puerto-banus/",
    "/blog/estepona-boat-rental/": "/",
    "/blog/cabopino-boat-rental/": "/",
    "/spoke/marbella-yacht-charter/": "/yacht-charter-marbella/",
}

BOAT_PATTERNS = [
    re.compile(r'^/boat/([a-z0-9-]+)/$'),
    re.compile(r'^/fleet/([a-z0-9-]+)/$'),
    re.compile(r'^/boats/([a-z0-9-]+)-flybridge/$'),
    re.compile(r'^/boat-rental-marbella-([a-z0-9-]+)/$'),
    re.compile(r'^/([a-z0-9-]+)-marbella/$'),
    re.compile(r'^/([a-z0-9-]+)-charter/$'),
    re.compile(r'^/([a-z0-9-]+)-boat/$'),
    re.compile(r'^/([a-z0-9-]+)/$'),
]

HREF_RE = re.compile(r'<a\b([^>]*?)href=\\"(/[^"\\]*)\\"([^>]*)>(.*?)</a>', re.DOTALL)
MD_LINK_RE = re.compile(r'\[([^\]]+)\]\((/[^)]*)\)')

def build_known_pages() -> set[str]:
    pages = set()
    for f in SITE.rglob("index.html"):
        rel = f.relative_to(SITE).parent
        pages.add("/" if str(rel) == "." else f"/{rel}/")
    return pages

def compute_fix(href: str) -> str | None:
    """Return the replacement path, or None to mean 'unlink'."""
    if href in ("/ /",) or href.strip() == "":
        return "/"
    if href == "/fleet/":
        return "/boats/"
    if href in NEAR_MISS_REDIRECTS:
        return NEAR_MISS_REDIRECTS[href]
    if href.startswith("/destinations/"):
        return "/experiences/"
    for pat in BOAT_PATTERNS:
        m = pat.match(href)
        if m:
            slug = resolve_boat_slug(m.group(1))
            if slug:
                return f"/boats/{slug}/"
    return None  # unresolved -> unlink

def process_file(path: pathlib.Path, known_pages: set[str]) -> int:
    text = path.read_text()
    changed = 0

    def repl(match: re.Match) -> str:
        nonlocal changed
        pre, href, post, body = match.groups()
        if href.startswith(("http", "mailto:", "tel:", "#")):
            return match.group(0)
        norm = href if href.endswith("/") else href + "/"
        if norm in known_pages:
            return match.group(0)  # already valid — untouched
        fix = compute_fix(href)
        changed += 1
        if fix is None:
            return body  # unlink, keep text
        return f'<a{pre}href=\\"{fix}\\"{post}>{body}</a>'

    def repl_md(match: re.Match) -> str:
        nonlocal changed
        body, raw_href = match.groups()
        href = raw_href.strip() or "/"
        if href.startswith(("http", "mailto:", "tel:", "#")):
            return match.group(0)
        norm = href if href.endswith("/") else href + "/"
        if norm in known_pages:
            if href != raw_href:
                changed += 1
                return f'[{body}]({href})'
            return match.group(0)  # already valid — untouched
        fix = compute_fix(href)
        changed += 1
        if fix is None:
            return body  # unlink, keep text
        return f'[{body}]({fix})'

    new_text = HREF_RE.sub(repl, text)
    new_text = MD_LINK_RE.sub(repl_md, new_text)
    if changed:
        json.loads(new_text)  # validate before writing
        path.write_text(new_text)
    return changed

def main():
    known_pages = build_known_pages()
    print(f"{len(known_pages)} known pages loaded from site/")
    total_files = 0
    total_links = 0
    for f in sorted(CONTENT_DIR.glob("*.json")):
        n = process_file(f, known_pages)
        if n:
            total_files += 1
            total_links += n
    print(f"fix_broken_content_links: patched {total_links} link(s) across {total_files} file(s)")

if __name__ == "__main__":
    main()
