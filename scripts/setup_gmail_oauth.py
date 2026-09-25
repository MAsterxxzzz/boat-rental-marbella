#!/usr/bin/env python3
"""
Gmail OAuth 2.0 Setup for Backlink Campaign
Handles user authorization and token storage.
"""

import json
import sys
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError

# Configuration
CONFIG_DIR = Path.home() / ".config" / "boathire-seo"
CREDENTIALS_FILE = CONFIG_DIR / "client_secrets.json"
TOKEN_FILE = CONFIG_DIR / "gmail_token.json"

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',  # Send emails
    'https://www.googleapis.com/auth/gmail.readonly',  # Read inbox (for monitoring)
]

OAUTH_SETUP_URL = """
📋 SETUP INSTRUCTIONS - GET YOUR OAUTH CREDENTIALS:

1. Go to Google Cloud Console:
   https://console.cloud.google.com/

2. Select project: boathire-seo

3. Navigate to "Credentials" (APIs & Services > Credentials)

4. Click "Create Credentials" → "OAuth 2.0 Client ID"

5. Choose application type: "Desktop application"

6. Click "Create"

7. Click the download icon to download the JSON file

8. Save it as:
   ~/.config/boathire-seo/client_secrets.json

Once saved, this script will open your browser for authorization.
"""


def print_setup_instructions():
    """Print setup instructions for getting OAuth credentials."""
    print(OAUTH_SETUP_URL)
    print("\nWaiting for client_secrets.json...")


def check_credentials_file():
    """Check if client_secrets.json exists."""
    if not CREDENTIALS_FILE.exists():
        print_setup_instructions()
        print(f"\n❌ File not found: {CREDENTIALS_FILE}")
        print(f"   Please download OAuth credentials from Google Cloud Console")
        print(f"   and save to: {CREDENTIALS_FILE}")
        sys.exit(1)
    print(f"✅ Found: {CREDENTIALS_FILE}")


def authorize_user():
    """Get user authorization via OAuth 2.0 flow."""
    print("\n🔐 Starting OAuth 2.0 Authorization Flow...")
    print("   Your browser will open in a moment...")

    # Check for existing token
    if TOKEN_FILE.exists():
        print(f"\n⚠️  Existing token found at {TOKEN_FILE}")
        response = input("   Proceed with existing token? (y/n): ").strip().lower()
        if response == 'y':
            with open(TOKEN_FILE, 'r') as f:
                return Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Create new authorization flow
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        SCOPES,
        redirect_uri='http://localhost:8080/'
    )

    print("\n📱 Opening browser for authorization...")
    print("   If browser doesn't open, visit the URL shown in terminal")

    try:
        creds = flow.run_local_server(port=8080)
    except Exception as e:
        print(f"\n❌ Authorization failed: {e}")
        sys.exit(1)

    # Save token for future use
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, 'w') as f:
        f.write(creds.to_json())

    print(f"\n✅ Authorization successful!")
    print(f"   Token saved to: {TOKEN_FILE}")

    return creds


def verify_token(creds):
    """Verify and refresh token if needed."""
    if creds.expired and creds.refresh_token:
        print("🔄 Refreshing access token...")
        try:
            creds.refresh(Request())
            print("✅ Token refreshed successfully")
        except RefreshError as e:
            print(f"❌ Token refresh failed: {e}")
            print("   Please run this script again to re-authorize")
            sys.exit(1)

    return creds


def send_test_email(creds):
    """Send a test email to verify Gmail API works."""
    import base64
    from email.mime.text import MIMEText
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from datetime import datetime

    print("\n📧 Sending test email...")

    recipient_email = "andra.kiirkivi@gmail.com"
    subject = "🚤 BoatHire Backlink Campaign — Gmail OAuth Test"
    body = f"""Hi Andra,

This test email confirms your Gmail OAuth 2.0 authentication is working! ✅

**Authorization Details:**
- Timestamp: {datetime.now().isoformat()}
- Account: andra.kiirkivi@gmail.com
- Scope: gmail.send (Send emails)
- Configuration: Local token stored in ~/.config/boathire-seo/gmail_token.json

**What's Next:**
Once this test email is received successfully (check your inbox), the backlink campaign will be ready to launch:

✓ Daily email scheduling (9 AM UTC)
✓ Automated personalized outreach
✓ Batch 2: Sep 5 (5 emails)
✓ Batch 3: Sep 12 (5 emails)
✓ Follow-ups: Sep 9, 16, 23
✓ Limit: Max 15 emails/day of qualified prospects

**Campaign Asset:**
https://boatrentalinmarbella.com/blog/boat-rental-marbella-price-index/

All future emails will include:
- Personalized subject lines (no mass templates)
- Custom body text per prospect (specific to their site/content)
- Relevant anchor text and positioning angle
- Tracking of all sends, responses, and acquired links

---

Best,
Andra Kiirkivi
Boat Rental Marbella
+358 400 406 194 (WhatsApp)

---
Test Email Verification
Sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
Gmail OAuth: Active & Verified
"""

    try:
        service = build('gmail', 'v1', credentials=creds)

        # Create email message
        message = MIMEText(body)
        message['To'] = recipient_email
        message['From'] = 'andra.kiirkivi@gmail.com'
        message['Subject'] = subject

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send message
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        message_id = result.get('id')
        print(f"\n✅ TEST EMAIL SENT SUCCESSFULLY")
        print(f"   Recipient: {recipient_email}")
        print(f"   Subject: {subject[:50]}...")
        print(f"   Message ID: {message_id}")

        return True, message_id

    except HttpError as e:
        print(f"\n❌ FAILED TO SEND TEST EMAIL")
        print(f"   Error Code: {e.resp.status}")
        print(f"   Error: {e.content.decode('utf-8') if e.content else str(e)}")
        return False, None

    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR")
        print(f"   {type(e).__name__}: {e}")
        return False, None


def main():
    """Run OAuth setup and test email."""
    print("=" * 80)
    print("GMAIL OAUTH 2.0 SETUP FOR BACKLINK CAMPAIGN")
    print("=" * 80)

    # Step 1: Check credentials file
    print("\n[1/4] Checking OAuth credentials...")
    check_credentials_file()

    # Step 2: Get authorization
    print("\n[2/4] Authorizing user...")
    creds = authorize_user()

    # Step 3: Verify token
    print("\n[3/4] Verifying token...")
    creds = verify_token(creds)

    # Step 4: Send test email
    print("\n[4/4] Sending test email...")
    success, message_id = send_test_email(creds)

    # Final status
    print("\n" + "=" * 80)
    if success:
        print("✅ GMAIL OAUTH SETUP COMPLETE")
        print("=" * 80)
        print(f"\n✨ Gmail API Integration Verified!")
        print(f"   Test Message ID: {message_id}")
        print(f"   Token Location: {TOKEN_FILE}")
        print(f"\n📊 Ready to launch 15/day backlink campaign")
        print(f"   Batch 2 (Sep 5): 5 Tier-2 prospects")
        print(f"   Batch 3 (Sep 12): 5 Tier-3 prospects")
        print(f"   Follow-ups: Sep 9, 16, 23 (max 2 per prospect)")
        print(f"\n🚀 Campaign will start automatically at 9 AM UTC daily")
        return 0
    else:
        print("❌ GMAIL OAUTH SETUP FAILED")
        print("=" * 80)
        print("\n⚠️  Please check the error above and try again")
        return 1


if __name__ == '__main__':
    sys.exit(main())
