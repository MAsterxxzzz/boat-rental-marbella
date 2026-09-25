#!/usr/bin/env python3
"""
Gmail API Email Sender for Backlink Campaign
Uses service account credentials from ~/.config/boathire-seo/service-account-key.json
Sends personalized backlink outreach emails.
"""

import json
import base64
import sys
from pathlib import Path
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

# Configuration
SERVICE_ACCOUNT_PATH = Path.home() / ".config" / "boathire-seo" / "service-account-key.json"
SENDER_EMAIL = "boatrentalinmarbella@gmail.com"
SENDER_NAME = "Andra Kiirkivi"
ASSET_URL = "https://boatrentalinmarbella.com/blog/boat-rental-marbella-price-index/"

# Gmail API scopes - includes sending emails as service account
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def load_credentials():
    """Load service account credentials from local JSON file."""
    if not SERVICE_ACCOUNT_PATH.exists():
        raise FileNotFoundError(
            f"Service account key not found at {SERVICE_ACCOUNT_PATH}\n"
            f"Expected: ~/.config/boathire-seo/service-account-key.json"
        )

    with open(SERVICE_ACCOUNT_PATH, 'r') as f:
        service_account_info = json.load(f)

    credentials = Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    return credentials


def send_email(recipient_email, recipient_name, subject, body):
    """Send email via Gmail API using service account."""
    try:
        credentials = load_credentials()

        # Create email message
        message = MIMEText(body)
        message['To'] = recipient_email
        message['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        message['Subject'] = subject

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Build Gmail API request
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        credentials.refresh(Request())
        service = build('gmail', 'v1', credentials=credentials)

        # Send message
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        return True, result.get('id', 'unknown')

    except Exception as e:
        return False, str(e)


def send_test_email(recipient_email="andra.kiirkivi@gmail.com"):
    """Send a single test email to verify Gmail API integration."""

    subject = "🚤 BoatHire Backlink Campaign Test — Gmail API Verification"

    body = f"""Hi there,

This is a TEST email from the BoatHire backlink campaign automation.

If you're reading this, it means the Gmail API integration is working correctly! ✅

**System Status:**
- Service Account: boathire-seo-agent
- Authentication: OAuth 2.0 (service account)
- Gmail Scope: gmail.send (verified)
- Sender: {SENDER_EMAIL}
- Test Email ID: {gen_test_id()}

**Next Steps:**
Once this test succeeds, the 15/day backlink outreach campaign will launch with:
- Batch 2: Sep 5 (5 emails to Tier 2 prospects)
- Batch 3: Sep 12 (5 emails to Tier 3 prospects)
- Follow-ups: Sep 9, 16, 23 (to non-respondents)
- Daily limit: Max 15 emails/day of qualified, personalized outreach

**Campaign Details:**
- Asset: {ASSET_URL}
- Current prospects: 15 in active rotation
- Tracking: Complete outreach log maintained

---

Best,
Andra Kiirkivi
Boat Rental Marbella
+358 400 406 194 (WhatsApp)

---
Test sent: {datetime.now().isoformat()}
"""

    print(f"📧 Sending test email to: {recipient_email}")
    print(f"   Subject: {subject}")

    success, result = send_email(recipient_email, "Test User", subject, body)

    if success:
        print(f"✅ TEST EMAIL SENT SUCCESSFULLY")
        print(f"   Message ID: {result}")
        print(f"\n🎉 Gmail API integration verified!")
        print(f"📊 Ready to launch 15/day backlink campaign")
        return True
    else:
        print(f"❌ FAILED TO SEND TEST EMAIL")
        print(f"   Error: {result}")
        return False


def gen_test_id():
    """Generate test email ID."""
    import time
    return f"test-{int(time.time())}"


if __name__ == "__main__":
    from datetime import datetime

    if len(sys.argv) > 1 and sys.argv[1] == "--recipient":
        recipient = sys.argv[2] if len(sys.argv) > 2 else "andra.kiirkivi@gmail.com"
        send_test_email(recipient)
    else:
        send_test_email()
