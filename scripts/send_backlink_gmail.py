#!/usr/bin/env python3
"""
Gmail API Email Sender for Backlink Campaign
Uses OAuth 2.0 token stored at ~/.config/boathire-seo/gmail_token.json
Sends personalized backlink outreach emails.
"""

import json
import base64
import sys
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
CONFIG_DIR = Path.home() / ".config" / "boathire-seo"
TOKEN_FILE = CONFIG_DIR / "gmail_token.json"
SENDER_EMAIL = "boatrentalinmarbella@gmail.com"
SENDER_NAME = "Andra Kiirkivi"
ASSET_URL = "https://boatrentalinmarbella.com/blog/boat-rental-marbella-price-index/"


def load_credentials():
    """Load OAuth 2.0 credentials from token file."""
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(
            f"Gmail token not found at {TOKEN_FILE}\n"
            f"Please run: python3 scripts/setup_gmail_oauth.py"
        )

    creds = Credentials.from_authorized_user_file(TOKEN_FILE)

    # Refresh token if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed token
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return creds


def send_email(recipient_email, recipient_name, subject, body):
    """Send email via Gmail API using OAuth 2.0."""
    try:
        creds = load_credentials()
        service = build('gmail', 'v1', credentials=creds)

        # Create email message
        message = MIMEText(body)
        message['To'] = recipient_email
        message['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        message['Subject'] = subject

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send message
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        return True, result.get('id', 'unknown')

    except HttpError as e:
        error_msg = e.content.decode('utf-8') if e.content else str(e)
        return False, f"HTTP {e.resp.status}: {error_msg}"
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)}"


def send_backlink_outreach(prospect):
    """Send personalized backlink outreach email to a prospect."""
    recipient_email = prospect.get('email')
    recipient_name = prospect.get('name')
    template = prospect.get('template', 'editorial')

    # Email templates (from automate_backlink_campaign.py)
    templates = {
        'editorial': {
            'subject': 'Marbella Boat Rental Guide — Unique Data Resource for Your Readers',
            'body': f"""Hi there,

I came across your comprehensive Marbella travel guide, and I noticed you cover outdoor activities and experiences.

We just published something I think your readers would find genuinely useful: the only publicly available boat rental price index for Marbella — comprehensive pricing data, seasonal trends, and cost breakdowns for yacht charters on the Costa del Sol.

Why your readers need this:
- Real market data (transparent, no marketing fluff)
- Historical pricing trends 2024-2026
- Price-per-person breakdowns for groups
- Clear cost drivers (fuel, skipper, insurance)
- Seasonal availability vs. pricing analysis

The resource: {ASSET_URL}

I'm wondering if this might fit naturally in your guide? It's the kind of practical, data-driven content your readers appreciate.

Happy to answer any questions.

Best,
Andra Kiirkivi
Boat Rental Marbella
💬 +358 400 406 194 (WhatsApp)""",
        },
        'influencer': {
            'subject': 'Boat Charter Pricing Guide — Resource for Your Marbella Guide',
            'body': f"""Hi {recipient_name.split()[0] if recipient_name else 'there'},

I follow your travel guides and noticed you have excellent coverage of Marbella activities. I have something that might be valuable for your readers planning a boat charter.

We published a Marbella Boat Rental Price Index — a transparent breakdown of real yacht charter pricing for the Costa del Sol. It includes:

✓ Current market rates (2026)
✓ Year-over-year pricing trends
✓ Price-per-person calculations for groups
✓ Seasonal availability (real data, not marketing)
✓ Budget to luxury tier comparisons

Why it fits your content:
Your audience appreciates luxury travel with transparency. This resource helps them understand what they're actually paying for (skipper, fuel, insurance included), and it shows budget-friendly options most luxury travel guides miss.

Link: {ASSET_URL}

Would this work as an update to your Marbella activities section? I'd love to see your readers get honest pricing data.

Best,
Andra Kiirkivi
Boat Rental Marbella""",
        },
        'platform': {
            'subject': 'Marbella Boat Charter Pricing Data — Authoritative Resource',
            'body': f"""Hi there,

We've compiled the only publicly-available boat rental pricing index for Marbella. This comprehensive market data includes:

• Current 2026 rates by boat tier
• Historical trends 2024-2026
• Seasonal availability analysis
• Port comparisons
• Group pricing breakdowns

This resource helps your users make informed decisions about boat charters on the Costa del Sol.

Resource: {ASSET_URL}

Would this be useful as a reference for your users?

Best,
Andra Kiirkivi
Boat Rental Marbella""",
        },
    }

    template_data = templates.get(template, templates['editorial'])
    subject = template_data['subject']
    body = template_data['body']

    return send_email(recipient_email, recipient_name, subject, body)


if __name__ == '__main__':
    # Example: Send email to a prospect
    if len(sys.argv) > 1:
        # Usage: python3 send_backlink_gmail.py <email> <name> <template>
        email = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else 'Prospect'
        template = sys.argv[3] if len(sys.argv) > 3 else 'editorial'

        prospect = {
            'email': email,
            'name': name,
            'template': template,
        }

        print(f"📧 Sending to {name} ({email})...")
        success, result = send_backlink_outreach(prospect)

        if success:
            print(f"✅ Email sent successfully")
            print(f"   Message ID: {result}")
        else:
            print(f"❌ Email send failed")
            print(f"   Error: {result}")
    else:
        print("Usage: python3 send_backlink_gmail.py <email> <name> [template]")
        print("Example: python3 send_backlink_gmail.py contact@example.com 'John Doe' editorial")
