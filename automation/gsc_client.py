#!/usr/bin/env python3
"""
Real Google Search Console API client.
Replaces the stub previously in daily_seo_agent.py, which checked only
whether the credentials file existed and returned hardcoded empty data.
"""

import logging
from pathlib import Path
from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build

logger = logging.getLogger('gsc_client')

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


class GSCClient:
    def __init__(self, service_account_path: Path, site_url: str):
        self.service_account_path = service_account_path
        self.site_url = site_url
        self._service = None

    def _get_service(self):
        if self._service is None:
            if not self.service_account_path.exists():
                raise FileNotFoundError(f"GSC credentials not found at {self.service_account_path}")
            creds = service_account.Credentials.from_service_account_file(
                str(self.service_account_path), scopes=SCOPES
            )
            self._service = build("searchconsole", "v1", credentials=creds)
        return self._service

    def fetch_search_analytics(self, days=28, dimensions=("query", "page"), row_limit=1000):
        """Pull real Search Analytics data for the last N days. Raises on failure — no silent fallback."""
        service = self._get_service()

        end_date = datetime.utcnow().date() - timedelta(days=3)  # GSC data has ~2-3 day lag
        start_date = end_date - timedelta(days=days)

        request_body = {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "dimensions": list(dimensions),
            "rowLimit": row_limit,
        }

        logger.info(f"Fetching GSC data: {start_date} to {end_date}, dims={dimensions}")
        response = service.searchanalytics().query(
            siteUrl=self.site_url, body=request_body
        ).execute()

        rows = response.get("rows", [])
        logger.info(f"GSC returned {len(rows)} rows")
        return {
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "dimensions": list(dimensions),
            "rows": rows,
            "fetched_at": datetime.utcnow().isoformat(),
        }


if __name__ == "__main__":
    import json
    logging.basicConfig(level=logging.INFO)
    sa_path = Path.home() / ".config" / "boathire-seo" / "service-account-key.json"
    client = GSCClient(sa_path, "sc-domain:boatrentalinmarbella.com")
    data = client.fetch_search_analytics(days=28, dimensions=("query", "page"))
    print(json.dumps(data, indent=2)[:3000])
