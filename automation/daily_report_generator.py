#!/usr/bin/env python3
"""
Daily SEO Report Generator
Creates human-readable daily summary from automation runs
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/daily_report.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('daily_report')

class DailyReportGenerator:
    """Generate daily SEO & automation report"""

    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.reports_dir = self.root / "reports"
        self.logs_dir = self.root / "logs"

    def generate_daily_report(self):
        """Create comprehensive daily report"""
        logger.info("=" * 70)
        logger.info("DAILY SEO & AUTOMATION REPORT")
        logger.info("=" * 70)

        report = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().date().isoformat(),
            "timezone": "UTC",
            "systems_checked": [],
            "metrics": {},
            "actions": [],
            "errors": [],
            "next_run": self._get_next_scheduled_run()
        }

        # Check SEO Agent
        seo_report_file = self.reports_dir / "daily_seo" / f"seo_report_{datetime.now().date().isoformat()}.json"
        if seo_report_file.exists():
            with open(seo_report_file) as f:
                seo_data = json.load(f)
            report["systems_checked"].append({
                "name": "Daily SEO Agent",
                "status": "✅ Executed",
                "file": str(seo_report_file),
                "opportunities_found": len(seo_data.get('opportunities', {})),
                "gsc_status": seo_data.get('status', 'unknown')
            })
            logger.info(f"✅ Daily SEO Agent: {seo_report_file.name}")
        else:
            report["errors"].append({
                "system": "Daily SEO Agent",
                "error": "No report file found",
                "expected_path": str(seo_report_file)
            })
            logger.warning(f"⚠️ No SEO report found: {seo_report_file}")

        # Check Backlink Outreach
        outreach_log_file = self.logs_dir / "backlink_outreach.log"
        if outreach_log_file.exists():
            with open(outreach_log_file) as f:
                log_content = f.read()
            email_count = log_content.count("EMAIL SENT")
            report["systems_checked"].append({
                "name": "Backlink Outreach Engine",
                "status": "✅ Executed" if email_count > 0 else "⚠️ Ready",
                "emails_sent_today": email_count,
                "file": str(outreach_log_file)
            })
            logger.info(f"✅ Backlink Outreach: {email_count} emails")
        else:
            logger.info("⚠️ No outreach log yet")

        # Check Weekly Review
        weekly_reports = list(self.reports_dir.glob("weekly_review_*.json"))
        if weekly_reports:
            latest = sorted(weekly_reports)[-1]
            report["systems_checked"].append({
                "name": "Weekly SEO Review",
                "status": "✅ Latest run",
                "file": str(latest)
            })
            logger.info(f"✅ Weekly Review: {latest.name}")

        # Summary
        logger.info("=" * 70)
        logger.info(f"Systems Checked: {len(report['systems_checked'])}")
        logger.info(f"Errors: {len(report['errors'])}")
        logger.info(f"Next Scheduled Run: {report['next_run']}")
        logger.info("=" * 70)

        # Save report
        report_file = self.reports_dir / f"daily_report_{datetime.now().date().isoformat()}.json"
        report_file.write_text(json.dumps(report, indent=2))
        logger.info(f"Report saved: {report_file}")

        return report

    def _get_next_scheduled_run(self):
        """Return next scheduled execution time"""
        now = datetime.utcnow()
        tomorrow_09 = (now + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
        if now.hour < 9:
            tomorrow_09 = now.replace(hour=9, minute=0, second=0, microsecond=0)

        return {
            "time": tomorrow_09.isoformat(),
            "timezone": "UTC",
            "systems": [
                "Daily SEO Agent (fetch GSC data)",
                "Backlink Outreach Engine (send emails)",
                "Weekly SEO Review (if Monday)"
            ]
        }

if __name__ == "__main__":
    generator = DailyReportGenerator()
    generator.generate_daily_report()
