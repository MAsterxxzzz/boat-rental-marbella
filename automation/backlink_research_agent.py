#!/usr/bin/env python3
"""
Daily backlink research agent.

Picks a small number of un-tracked candidates from data/prospect_seed_candidates.csv,
fetches their real page content, and asks an LLM (Anthropic API) to:
  1. extract a real contact email/phone ONLY if actually present in the fetched text
     (never invented)
  2. judge genuine relevance to Boat Rental Marbella
  3. draft a short, specific, personalized outreach email if (1) and (2) succeed

Writes verified prospects to data/backlink_prospects.csv and drafts to
reports/pending_outreach/ — NEVER sends anything. Sending remains a separate,
explicitly human-approved step.

Requires ANTHROPIC_API_KEY env var. If absent, logs a clear warning and exits
cleanly (does not fabricate results).
"""
import csv
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler('logs/backlink_research_agent.log'), logging.StreamHandler()],
)
logger = logging.getLogger('backlink_research_agent')

ROOT = Path(__file__).parent.parent
SEED_FILE = ROOT / "data" / "prospect_seed_candidates.csv"
TRACKER_FILE = ROOT / "data" / "backlink_prospects.csv"
PENDING_DIR = ROOT / "reports" / "pending_outreach"
MAX_NEW_PER_RUN = 2

TRACKER_FIELDS = [
    "domain", "company", "category", "contact_name", "contact_email", "source_url",
    "relevance_reason", "date_found", "date_contacted", "follow_up_1_date",
    "follow_up_2_date", "reply_status", "reply_date", "backlink_status",
    "backlink_url", "verified",
]


def load_business_facts():
    cfg = json.loads((ROOT / "config" / "keyword_map.json").read_text())["site"]
    return (
        f"Business: {cfg['name']}, based in Marbella, departing {', '.join(cfg['departure_ports'])}. "
        f"Fleet includes an Astondoa 40 and Azimut 39 (12.5m motor yachts), pricing from "
        f"EUR{cfg['price_anchor_low_2h']}/2h to EUR{cfg['price_anchor_fullday_8h']}/8h. "
        f"Contact: WhatsApp {cfg['whatsapp_e164']}, email {cfg['email']}. Website: {cfg['base_url']}"
    )


def fetch_page_text(url, timeout=15):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; BRM-research-agent/1.0)"})
    with urlopen(req, timeout=timeout) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:8000]


def call_anthropic(page_text, company, business_facts, api_key):
    prompt = f"""You are researching a potential local partner for a Marbella boat charter business.

{business_facts}

Below is the real, live text content of {company}'s website. Based ONLY on what appears in this text:

1. Is there a real contact email address or phone number literally present in this text? Quote it exactly if so. If none is visible, say "none found" — do not guess or construct one.
2. Is this business genuinely relevant as a local partner (e.g. would plausibly refer clients toward a boat charter: hotels, concierges, wedding/event planners, villa rental, marina services, travel agencies — NOT a direct boat rental/yacht charter competitor)? Answer yes/no with a one-sentence reason grounded in the text.
3. If relevance is yes AND a real contact exists, draft a short (under 120 words), specific, non-generic outreach email referencing something concrete from their actual page content. If either condition fails, write "SKIP".

Respond as JSON only, no other text:
{{"contact_email_or_phone": "...", "relevant": true/false, "relevance_reason": "...", "email_subject": "...", "email_body": "..."}}

Website text:
{page_text}
"""
    body = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 700,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    req = Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    with urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    text = result["content"][0]["text"]
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError(f"No JSON found in model response: {text[:200]}")
    return json.loads(match.group(0))


def load_tracked_domains():
    if not TRACKER_FILE.exists():
        return set()
    with open(TRACKER_FILE) as f:
        return {row["domain"] for row in csv.DictReader(f)}


def append_to_tracker(row):
    exists = TRACKER_FILE.exists()
    with open(TRACKER_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def run():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.warning("ANTHROPIC_API_KEY not set — skipping backlink research today. "
                        "No prospects fabricated, no drafts written.")
        return {"status": "skipped_no_api_key", "new_prospects": 0}

    if not SEED_FILE.exists():
        logger.warning(f"No seed candidates file at {SEED_FILE}")
        return {"status": "no_seed_file", "new_prospects": 0}

    with open(SEED_FILE) as f:
        candidates = list(csv.DictReader(f))

    tracked = load_tracked_domains()
    untracked = [c for c in candidates if c["domain"] not in tracked]
    todays_batch = untracked[:MAX_NEW_PER_RUN]

    if not todays_batch:
        logger.info("No new untracked candidates in seed file today.")
        return {"status": "no_new_candidates", "new_prospects": 0}

    business_facts = load_business_facts()
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.utcnow().date().isoformat()
    results = []

    for cand in todays_batch:
        logger.info(f"Researching {cand['company']} ({cand['candidate_url']})...")
        try:
            page_text = fetch_page_text(cand["candidate_url"])
        except Exception as e:
            logger.error(f"Fetch failed for {cand['candidate_url']}: {e}")
            continue

        try:
            verdict = call_anthropic(page_text, cand["company"], business_facts, api_key)
        except Exception as e:
            logger.error(f"Anthropic API call failed for {cand['company']}: {e}")
            continue

        contact = verdict.get("contact_email_or_phone", "")
        relevant = verdict.get("relevant", False)
        if not relevant or not contact or contact.lower() == "none found":
            logger.info(f"SKIP {cand['company']}: relevant={relevant}, contact={contact!r}")
            continue

        append_to_tracker({
            "domain": cand["domain"], "company": cand["company"], "category": cand["category"],
            "contact_name": "", "contact_email": contact, "source_url": cand["candidate_url"],
            "relevance_reason": verdict.get("relevance_reason", ""), "date_found": today,
            "date_contacted": "", "follow_up_1_date": "", "follow_up_2_date": "",
            "reply_status": "not_contacted", "reply_date": "", "backlink_status": "not_sent",
            "backlink_url": "", "verified": "true",
        })

        draft_file = PENDING_DIR / f"{today}_{cand['domain']}.json"
        draft_file.write_text(json.dumps({
            "company": cand["company"], "domain": cand["domain"], "contact": contact,
            "subject": verdict.get("email_subject", ""), "body": verdict.get("email_body", ""),
            "relevance_reason": verdict.get("relevance_reason", ""),
            "source_url": cand["candidate_url"], "drafted_date": today, "status": "pending_review",
        }, indent=2))

        logger.info(f"NEW VERIFIED PROSPECT: {cand['company']} — draft saved to {draft_file}, NOT sent")
        results.append(cand["company"])

    return {"status": "ok", "new_prospects": len(results), "companies": results}


if __name__ == "__main__":
    result = run()
    logger.info(f"Backlink research agent complete: {result}")
