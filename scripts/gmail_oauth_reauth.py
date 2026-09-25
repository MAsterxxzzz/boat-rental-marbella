#!/usr/bin/env python3
"""
Re-authorize the boatrentalinmarbella@gmail.com Gmail OAuth token via a local
browser consent flow, then verify access WITHOUT sending any email.

Saves the token in the standard google-auth Credentials.to_json() format
(includes client_id/client_secret/token_uri), fixing a prior format mismatch
where the file only had a raw token-exchange dump.

Never prints token/credential values — only status.
"""
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CONFIG_DIR = Path.home() / ".config" / "boathire-seo"
CREDENTIALS_FILE = CONFIG_DIR / "client_secrets.json"
TOKEN_FILE = CONFIG_DIR / "gmail_token.json"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]
EXPECTED_EMAIL = "boatrentalinmarbella@gmail.com"


def main():
    if not CREDENTIALS_FILE.exists():
        print(f"❌ Missing {CREDENTIALS_FILE} — cannot proceed.")
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
    print("AUTH_URL_START")
    creds = flow.run_local_server(port=8080, prompt="consent", open_browser=False)
    print("AUTH_URL_END")

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(creds.to_json())
    print(f"✅ New token saved to {TOKEN_FILE} (standard format, not printed here).")

    # Verify via a READ-ONLY call — do not send anything.
    service = build("gmail", "v1", credentials=creds)
    profile = service.users().getProfile(userId="me").execute()
    authenticated_email = profile.get("emailAddress")

    print(f"Authenticated as: {authenticated_email}")
    if authenticated_email != EXPECTED_EMAIL:
        print(f"⚠️  WARNING: authenticated account does not match expected {EXPECTED_EMAIL}")
    else:
        print(f"✅ Confirmed correct account: {EXPECTED_EMAIL}")

    print(f"Messages total (readonly access proof): {profile.get('messagesTotal')}")
    print(f"Granted scopes: {creds.scopes}")
    print("gmail.send" in " ".join(creds.scopes or []) and "✅ gmail.send scope present (authorized to send — nothing sent by this script)"
          or "❌ gmail.send scope NOT present")


if __name__ == "__main__":
    main()
