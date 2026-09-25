#!/usr/bin/env python3
"""
Send test email via Resend API
Verifies email sending works before launching 15/day campaign
"""

import json
import pathlib
import urllib.request
import urllib.error
from datetime import datetime

# Load API key from .env
ROOT = pathlib.Path(__file__).resolve().parents[1]
key = None
for line in (ROOT / ".env").read_text().splitlines():
    if line.startswith("RESEND_API_KEY="):
        key = line.split("=", 1)[1].strip()

if not key:
    print("❌ RESEND_API_KEY not found in .env")
    exit(1)

# Email details
FROM = "Andra Kiirkivi <boatrentalinmarbella@gmail.com>"
TO = "andra.kiirkivi@gmail.com"
SUBJECT = "🚤 BoatHire Backlink Campaign — Resend API Test"
BODY = f"""Hi Andra,

This test email confirms your Resend API integration is working! ✅

**Email Sending Verification:**
- Timestamp: {datetime.now().isoformat()}
- From: boatrentalinmarbella@gmail.com
- To: andra.kiirkivi@gmail.com
- Provider: Resend API
- Status: Sent successfully

**Campaign Ready:**
Once you confirm this email arrived, the 15/day backlink campaign will launch with:

✓ Batch 2 (Sep 5): 5 Tier-2 prospects
✓ Batch 3 (Sep 12): 5 Tier-3 prospects
✓ Follow-ups: Sep 9, 16, 23 (max 2 per prospect)
✓ Daily limit: Max 15 personalized emails/day
✓ No mass templates — every email unique

**Campaign Asset:**
https://boatrentalinmarbella.com/blog/boat-rental-marbella-price-index/

---

Best,
Andra Kiirkivi
Boat Rental Marbella
+358 400 406 194 (WhatsApp)
"""

# Send via Resend API
print("📧 Sending test email via Resend API...")
print(f"   To: {TO}")

request_body = json.dumps({
    "from": FROM,
    "to": TO,
    "subject": SUBJECT,
    "text": BODY,
}).encode()

req = urllib.request.Request(
    "https://api.resend.com/emails",
    data=request_body,
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "BoatRentalMarbella/1.0",
    },
)

try:
    with urllib.request.urlopen(req) as r:
        resp = json.load(r)
        message_id = resp.get('id')
        print(f"\n✅ TEST EMAIL SENT SUCCESSFULLY")
        print(f"   Message ID: {message_id}")
        print(f"\n🎉 Resend API Integration Verified!")
        print(f"📊 Ready to launch 15/day backlink campaign")
        print(f"\n✨ Check your inbox for the test email confirmation")

except urllib.error.HTTPError as e:
    error_content = e.read().decode()
    print(f"\n❌ FAILED TO SEND TEST EMAIL")
    print(f"   HTTP {e.code}")
    print(f"   Error: {error_content[:300]}")
    exit(1)

except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR")
    print(f"   {type(e).__name__}: {e}")
    exit(1)
