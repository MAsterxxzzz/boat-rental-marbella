#!/usr/bin/env python3
"""
DAILY SEO AGENT FOR BOAT RENTAL MARBELLA
Pulls real Google Search Console data via gsc_client.GSCClient, identifies
concrete opportunities, and appends justified, deduplicated tasks to a
persistent backlog (reports/backlog.json) for review/implementation.

This agent does NOT edit site content automatically. It records findings.
Implementation of substantial page changes goes through reviewable commits,
not unattended daily edits to business content.
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from gsc_client import GSCClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/daily_seo_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('daily_seo_agent')


class DailySEOAgent:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.config = json.loads((self.root / "config" / "keyword_map.json").read_text())
        self.base_url = self.config["site"]["base_url"]
        self.site_property = "sc-domain:boatrentalinmarbella.com"
        self.gsc_sa_path = Path.home() / ".config" / "boathire-seo" / "service-account-key.json"
        self.report_dir = self.root / "reports" / "daily_seo"
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.backlog_path = self.root / "reports" / "backlog.json"

        logger.info(f"Daily SEO Agent initialized for {self.base_url}")

    def get_gsc_data(self):
        """Pull real Search Analytics data. Returns None (not fake data) on failure."""
        logger.info("Fetching Google Search Console data...")
        try:
            client = GSCClient(self.gsc_sa_path, self.site_property)
            data = client.fetch_search_analytics(days=28, dimensions=("query", "page"))
            logger.info(f"GSC fetch OK: {len(data['rows'])} rows, {data['period_start']} to {data['period_end']}")
            return data
        except FileNotFoundError as e:
            logger.error(f"GSC credentials missing: {e}")
            return None
        except Exception as e:
            logger.error(f"GSC data fetch failed: {e}")
            return None

    def analyze_opportunities(self, gsc_data):
        """Turn raw GSC rows into concrete, page-mapped opportunities. No invented numbers."""
        if not gsc_data or not gsc_data.get("rows"):
            logger.warning("No GSC data available for analysis")
            return {"ranking_opportunities": [], "zero_click_high_impression": [], "by_page": {}}

        by_page = defaultdict(list)
        for row in gsc_data["rows"]:
            query, page = row["keys"]
            by_page[page].append({
                "query": query,
                "clicks": row["clicks"],
                "impressions": row["impressions"],
                "ctr": row["ctr"],
                "position": round(row["position"], 1),
            })

        ranking_opportunities = []  # impressions >= 3, position between 11-100 (not page 1) = room to climb
        zero_click_high_impression = []  # impressions >= 5, clicks == 0

        for page, rows in by_page.items():
            for r in rows:
                if r["impressions"] >= 3 and r["position"] > 10:
                    ranking_opportunities.append({**r, "page": page})
                if r["impressions"] >= 5 and r["clicks"] == 0:
                    zero_click_high_impression.append({**r, "page": page})

        ranking_opportunities.sort(key=lambda x: -x["impressions"])
        zero_click_high_impression.sort(key=lambda x: -x["impressions"])

        logger.info(
            f"Found {len(ranking_opportunities)} ranking opportunities, "
            f"{len(zero_click_high_impression)} zero-click high-impression queries, "
            f"across {len(by_page)} pages"
        )

        return {
            "ranking_opportunities": ranking_opportunities[:30],
            "zero_click_high_impression": zero_click_high_impression[:30],
            "by_page": {k: v for k, v in by_page.items()},
        }

    def _load_backlog(self):
        if self.backlog_path.exists():
            return json.loads(self.backlog_path.read_text())
        return {"items": [], "last_updated": None}

    def _save_backlog(self, backlog):
        backlog["last_updated"] = datetime.utcnow().isoformat()
        self.backlog_path.write_text(json.dumps(backlog, indent=2))

    def update_backlog(self, opportunities):
        """Append newly-identified, deduplicated tasks to the persistent backlog.
        Never re-adds a (page, query) pair already tracked, regardless of status."""
        backlog = self._load_backlog()
        existing_keys = {(item["page"], item["query"]) for item in backlog["items"]}

        added = 0
        for opp in opportunities["ranking_opportunities"][:15]:
            key = (opp["page"], opp["query"])
            if key in existing_keys:
                continue
            backlog["items"].append({
                "id": f"rank-{len(backlog['items'])+1}",
                "type": "ranking_opportunity",
                "page": opp["page"],
                "query": opp["query"],
                "impressions": opp["impressions"],
                "position": opp["position"],
                "status": "identified",
                "identified_date": datetime.utcnow().date().isoformat(),
                "notes": f"{opp['impressions']} impressions/28d at position {opp['position']} — not on page 1",
            })
            existing_keys.add(key)
            added += 1

        logger.info(f"Backlog: {added} new items added, {len(backlog['items'])} total tracked")
        self._save_backlog(backlog)
        return backlog, added

    def select_todays_tasks(self, backlog, max_tasks=3):
        """Pick a small number of 'identified' backlog items to flag for action today.
        Does not implement changes — surfaces them for review, per the no-unattended-content-edits rule."""
        candidates = [i for i in backlog["items"] if i["status"] == "identified"]
        candidates.sort(key=lambda x: -x["impressions"])
        selected = candidates[:max_tasks]
        for item in selected:
            item["status"] = "selected_for_review"
            item["selected_date"] = datetime.utcnow().date().isoformat()
        return selected

    def generate_daily_report(self, opportunities, backlog, selected_tasks, gsc_status):
        report_date = datetime.utcnow().date().isoformat()
        report_file = self.report_dir / f"seo_report_{report_date}.json"

        report = {
            "date": report_date,
            "timestamp": datetime.utcnow().isoformat(),
            "gsc_status": gsc_status,
            "opportunities_found": {
                "ranking_opportunities": len(opportunities.get("ranking_opportunities", [])),
                "zero_click_high_impression": len(opportunities.get("zero_click_high_impression", [])),
            },
            "top_ranking_opportunities": opportunities.get("ranking_opportunities", [])[:10],
            "backlog_total_items": len(backlog["items"]),
            "tasks_selected_today": selected_tasks,
            "status": "ACTIVE" if gsc_status == "ok" else "DEGRADED_NO_GSC_DATA",
        }

        report_file.write_text(json.dumps(report, indent=2))
        logger.info(f"Report saved: {report_file}")
        return report_file

    def run(self):
        logger.info("=" * 60)
        logger.info("DAILY SEO AGENT - EXECUTION START")
        logger.info("=" * 60)

        gsc_data = self.get_gsc_data()
        gsc_status = "ok" if gsc_data else "failed"

        opportunities = self.analyze_opportunities(gsc_data)
        backlog, added = self.update_backlog(opportunities)
        selected = self.select_todays_tasks(backlog)
        self._save_backlog(backlog)

        report_file = self.generate_daily_report(opportunities, backlog, selected, gsc_status)

        logger.info("=" * 60)
        logger.info(f"DAILY SEO AGENT - EXECUTION COMPLETE (gsc_status={gsc_status})")
        logger.info("=" * 60)

        return report_file


if __name__ == "__main__":
    agent = DailySEOAgent()
    result = agent.run()
    if result is None:
        sys.exit(1)
