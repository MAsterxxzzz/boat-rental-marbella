#!/usr/bin/env python3
"""Prints a concise markdown daily summary for today's SEO + crawl reports.
Used by .github/workflows/seo-daily.yml to populate GITHUB_STEP_SUMMARY.
Safe to run locally too — just prints to stdout.
"""
import json
from datetime import datetime
from pathlib import Path

root = Path(__file__).parent.parent
today = datetime.utcnow().date().isoformat()

print(f"## Daily SEO run — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")

seo_report = root / "reports" / "daily_seo" / f"seo_report_{today}.json"
print("### GSC / keyword findings")
if seo_report.exists():
    r = json.loads(seo_report.read_text())
    print(f"- GSC status: {r['gsc_status']}")
    print(f"- Ranking opportunities found: {r['opportunities_found']['ranking_opportunities']}")
    print(f"- Zero-click high-impression queries: {r['opportunities_found']['zero_click_high_impression']}")
    print(f"- Backlog total tracked items: {r['backlog_total_items']}")
    if r.get("by_language"):
        print(f"- By language (heuristic ES-detector, not a real classifier): "
              + ", ".join(f"{k}: {v['impressions']} impr / {v['queries']} queries" for k, v in r["by_language"].items()))
    if r.get("by_country"):
        top_countries = list(r["by_country"].items())[:5]
        print(f"- Top countries by impressions: " + ", ".join(f"{c}:{n}" for c, n in top_countries))
    if r.get("language_mismatches"):
        print(f"- Spanish-language queries landing on a non-/es/ page: {len(r['language_mismatches'])}")
        for m in r["language_mismatches"][:5]:
            print(f"  - \"{m['query']}\" -> {m['page']} ({m['impressions']} impr)")
    print(f"- Tasks selected today: {len(r['tasks_selected_today'])}")
    for t in r["tasks_selected_today"]:
        print(f"  - \"{t['query']}\" on {t['page']} ({t['impressions']} impr, pos {t['position']})")
else:
    print("- No SEO report generated this run (see logs/daily_seo_agent.log)")

print()
crawl_report = root / "reports" / "technical_crawl" / f"crawl_report_{today}.json"
print("### Technical crawl findings")
if crawl_report.exists():
    r = json.loads(crawl_report.read_text())
    print(f"- HTML validity issues (best-effort, needs manual review): {len(r['html_validity_issues'])} files flagged")
    broken = sum(len(v) for v in r["broken_internal_links"].values())
    print(f"- Broken internal links: {broken} across {len(r['broken_internal_links'])} files")
    print(f"- Duplicate titles: {len(r['duplicate_titles'])} title(s) shared across multiple pages")
    hc = r.get("hreflang_canonical", {})
    print(f"- hreflang/canonical issues: {len(hc.get('issues', []))} across {len(hc.get('pages_checked', []))} language homepages checked")
    sm = r["sitemap"]
    print(f"- Sitemap: exists={sm.get('exists')}, valid_xml={sm.get('valid_xml')}, "
          f"url_count={sm.get('url_count')}, missing_on_disk={sm.get('urls_missing_count')}")
else:
    print("- No technical crawl report generated this run (see logs/technical_crawl.log)")
