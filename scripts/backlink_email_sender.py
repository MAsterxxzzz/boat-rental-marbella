#!/usr/bin/env python3
"""
Backlink Campaign Email Sender (Resend API)
Sends personalized outreach emails to backlink prospects
"""

import json
import pathlib
import urllib.request
import urllib.error
import sys

# Load Resend API key
ROOT = pathlib.Path(__file__).resolve().parents[1]
RESEND_KEY = None
for line in (ROOT / ".env").read_text().splitlines():
    if line.startswith("RESEND_API_KEY="):
        RESEND_KEY = line.split("=", 1)[1].strip()

if not RESEND_KEY:
    raise SystemExit("❌ RESEND_API_KEY not found in .env")

# Campaign configuration
FROM = "Andra Kiirkivi <info@boathire24.com>"
REPLY_TO = "info@boathire24.com"
ASSET_URL = "https://boatrentalinmarbella.com/blog/boat-rental-marbella-price-index/"

# Email templates (from automate_backlink_campaign.py)
EMAIL_TEMPLATES = {
    "editorial": {
        "subject": "Marbella Boat Rental Guide — Unique Data Resource for Your Readers",
        "body": """Hi there,

I came across your comprehensive Marbella travel guide, and I noticed you cover outdoor activities and experiences.

We just published something I think your readers would find genuinely useful: the only publicly available boat rental price index for Marbella — comprehensive pricing data, seasonal trends, and cost breakdowns for yacht charters on the Costa del Sol.

Why your readers need this:
- Real market data (transparent, no marketing fluff)
- Historical pricing trends 2024-2026
- Price-per-person breakdowns for groups
- Clear cost drivers (fuel, skipper, insurance)
- Seasonal availability vs. pricing analysis

The resource: {asset_url}

I'm wondering if this might fit naturally in your guide? It's the kind of practical, data-driven content your readers appreciate.

Happy to answer any questions.

Best,
Andra Kiirkivi
Boat Rental Marbella
💬 +358 400 406 194 (WhatsApp)""",
    },
    "influencer": {
        "subject": "Boat Charter Pricing Guide — Resource for Your Marbella Guide",
        "body": """Hi {name},

I follow your travel guides and noticed you have excellent coverage of Marbella activities. I have something that might be valuable for your readers planning a boat charter.

We published a Marbella Boat Rental Price Index — a transparent breakdown of real yacht charter pricing for the Costa del Sol. It includes:

✓ Current market rates (2026)
✓ Year-over-year pricing trends
✓ Price-per-person calculations for groups
✓ Seasonal availability (real data, not marketing)
✓ Budget to luxury tier comparisons

Why it fits your content:
Your audience appreciates luxury travel with transparency. This resource helps them understand what they're actually paying for (skipper, fuel, insurance included), and it shows budget-friendly options most luxury travel guides miss.

Link: {asset_url}

Would this work as an update to your Marbella activities section? I'd love to see your readers get honest pricing data.

Best,
Andra Kiirkivi
Boat Rental Marbella""",
    },
    "niche_yacht": {
        "subject": "Marbella Boat Rental Market Report — Charter Pricing Data",
        "body": """Hi Editorial Team,

Boat International covers yacht charter destinations globally. I thought you might find our Marbella market research valuable for your destination guides.

We've compiled comprehensive 2026 pricing data for Marbella boat charters, including:

• Current market rates across boat tiers (budget to superyacht)
• Year-over-year pricing trends (2024-2026)
• Charter cost analysis and market drivers
• Seasonal availability breakdown
• Port comparisons (Marbella, Puerto Banús, other Costa del Sol)

Market insight: Superyacht segment up 12.4% over 2 years (demand-driven), while budget segment remains stable.

This is the only publicly published pricing index for Marbella charters.

Resource: {asset_url}

Would this be useful as a reference for your destination guide?

Best,
Andra Kiirkivi
Boat Rental Marbella""",
    },
    "events": {
        "subject": "Boat Party Pricing Guide — Resource for Your Marbella Experiences",
        "body": """Hi Team,

Your Marbella hen party and event guides are popular. I wanted to share a resource that might be useful for your readers planning boat parties in Marbella.

We published a Marbella boat rental price index that breaks down exactly what group boat charters cost. It includes:

✓ Group pricing (2-10+ people)
✓ Duration options (2h, 4h, 8h charters)
✓ Cost-per-person calculations
✓ Budget-friendly entry options (from €230)
✓ Luxury packages for premium events

For hen and stag parties, boat charters are ideal — and our pricing transparency helps groups understand their actual costs before committing.

Resource: {asset_url}

Would you link to this from your Marbella experiences section?

Best,
Andra Kiirkivi
Boat Rental Marbella""",
    },
    "weddings": {
        "subject": "Marbella Destination Wedding Resource — Boat Charter Guide",
        "body": """Hi Junebug Team,

Your destination wedding guides for Spain are excellent. I have a resource specifically for couples planning rehearsal activities or intimate experiences in Marbella.

We published a Marbella boat rental price index that wedding planners and couples find valuable:

• Transparent pricing for boat charters
• Group pricing for wedding parties (10-12 people)
• Duration options for rehearsal activities
• Luxury tier options for memorable experiences
• Real cost breakdowns (no hidden fees)

For destination weddings in Marbella: A boat charter works as a rehearsal dinner alternative, bachelor/bachelorette activity, or intimate celebration. Our pricing guide helps couples budget accurately.

Resource: {asset_url}

Would this be useful in your destination wedding guides?

Best,
Andra Kiirkivi
Boat Rental Marbella""",
    },
    "platform": {
        "subject": "Marbella Boat Charter Pricing Data — Authoritative Resource",
        "body": """Hi there,

We've compiled the only publicly-available boat rental pricing index for Marbella. This comprehensive market data includes:

• Current 2026 rates by boat tier
• Historical trends 2024-2026
• Seasonal availability analysis
• Port comparisons
• Group pricing breakdowns

This resource helps your users make informed decisions about boat charters on the Costa del Sol.

Resource: {asset_url}

Would this be useful as a reference for your users?

Best,
Andra Kiirkivi
Boat Rental Marbella""",
    },
    "vacation_rental": {
        "subject": "Boat Charter Activities — Resource for Your Villa Renters",
        "body": """Hi there,

Your villa rental guests often ask about boat charter activities in Marbella. We published a comprehensive pricing guide that helps travelers understand real costs.

The Marbella Boat Rental Price Index includes:

• Transparent pricing (no hidden fees)
• Group pricing for villa parties
• Duration options (2h to full day)
• Real guest reviews and experiences
• Seasonal availability guide

This resource helps your guests plan their vacation activities and budget accurately.

Resource: {asset_url}

Would this be useful for your guest guides or activity recommendations?

Best,
Andra Kiirkivi
Boat Rental Marbella""",
    },
    "government": {
        "subject": "Marbella Boat Charter Market Data — Tourism Resource",
        "body": """Hi there,

We've compiled the only publicly published boat rental pricing index for Marbella. As an official tourism resource, you might find this market data valuable for your destination guides and visitor planning.

The index includes comprehensive 2026 pricing data, seasonal trends, and cost breakdowns for yacht charters on the Costa del Sol.

Resource: {asset_url}

Would this resource be useful for your tourism guides?

Best,
Andra Kiirkivi
Boat Rental Marbella""",
    },
    "forum": {
        "subject": "Marbella Boat Charter Pricing Index",
        "body": """Hi,

We've published the only publicly available boat rental pricing index for Marbella. This might be useful for your forum members planning charters.

The index includes current rates, historical trends, seasonal analysis, and group pricing breakdowns.

Resource: {asset_url}

Best,
Andra Kiirkivi
Boat Rental Marbella""",
    },
}


def send_email(recipient_email, recipient_name, subject, body):
    """Send email via Resend API"""
    request_body = json.dumps({
        "from": FROM,
        "to": recipient_email,
        "reply_to": REPLY_TO,
        "subject": subject,
        "text": body,
    }).encode()

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=request_body,
        headers={
            "Authorization": f"Bearer {RESEND_KEY}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req) as r:
            resp = json.load(r)
            return True, resp.get('id')
    except urllib.error.HTTPError as e:
        error = e.read().decode()
        return False, error
    except Exception as e:
        return False, str(e)


def send_outreach_email(prospect):
    """Send personalized outreach email to a prospect"""
    recipient_email = prospect.get('email')
    recipient_name = prospect.get('name')
    template_name = prospect.get('template', 'editorial')

    template = EMAIL_TEMPLATES.get(template_name, EMAIL_TEMPLATES['editorial'])
    subject = template['subject']
    body = template['body'].format(
        asset_url=ASSET_URL,
        name=recipient_name.split()[0] if recipient_name else 'there'
    )

    return send_email(recipient_email, recipient_name, subject, body)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 backlink_email_sender.py <email> <name> [template]")
        print("Example: python3 backlink_email_sender.py contact@example.com 'John Doe' editorial")
        sys.exit(1)

    email = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else 'Prospect'
    template = sys.argv[3] if len(sys.argv) > 3 else 'editorial'

    prospect = {'email': email, 'name': name, 'template': template}

    print(f"📧 Sending to {name} ({email})...")
    success, result = send_outreach_email(prospect)

    if success:
        print(f"✅ Email sent successfully")
        print(f"   Message ID: {result}")
    else:
        print(f"❌ Email send failed")
        print(f"   Error: {result}")
