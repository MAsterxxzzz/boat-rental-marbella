# Safer wording for approval — nothing below has been applied
**Why:** none of these claims can be proven from the repository data. Reply-time and "verified" claims appear on **862 of 1,257 pages** because they come from shared templates (`templates/page.html.template`, `scripts/build_es.py`, `build_de.py`, `build_uk.py`), so changing them is a **bulk change** and needs your approval. Proposed method: edit the templates, regenerate, review the diff, deploy once, verify live.

## A. Reply-time claims (no data supports any number)
| Where it appears now | Pages | Proposed replacement |
|---|---|---|
| "💬 WhatsApp reply in <5 min" (trust bar) | 854 | "💬 Quotes on WhatsApp" |
| "Avg reply < 5 min · No deposit until you confirm" (booking card) | 853 | "Quote on WhatsApp · [deposit wording, see C]" |
| "we'll reply on WhatsApp within 5 minutes with available boats & final price" (booking form) | 853 | "we'll reply on WhatsApp with available boats & the final price" |
| "get a live availability quote within 5 minutes" (homepage, 2 pages) | 2 | "get a quote on WhatsApp" |
| "Average WhatsApp reply < 5 minutes" / "average reply under 5 minutes" (contact, cancellation, booking modal) | several | "WhatsApp is the fastest way to reach us" (the contact page already says this) |
| Email "typical reply within 4 hours" (contact) | 1 | remove the number, or keep **only if** you confirm it |
**If you can state a real figure** (for example "we reply within 30 minutes, 09:00–21:00 Spain time"), tell me the figure and the hours and I will use it exactly. Keep it as a stated service hour, not an "average".

## B. Review claims (`config/reviews.json` calls them "curated"; 20 reviews, 4.9, dated 2026-01..05)
| Now | Pages | Proposed |
|---|---|---|
| "4.9 · verified reviews" / "Read our verified reviews" (aria-label) | 860 | "4.9 · 20 guest reviews" |
| "4.9-star average on verified reviews. Real guests sharing real moments — no fake testimonials" | homepage | "4.9 average from 20 guest reviews" — and drop "no fake testimonials" unless you confirm every review is real and tell me where each came from |
| "take a look at 20 verified guest reviews" (contact) | 1 | "take a look at our 20 guest reviews" |
**Needed from you:** confirm the 20 reviews are from real customers, and where they were collected (Google, Click&Boat, WhatsApp, email). If any are not real or not yours, they must be removed before any rating markup is used. Rating markup stays only on `/reviews/`.

## C. Other claims I found that I cannot prove (please confirm or give me wording)
- "No deposit until you confirm" (booking card/modal). Check against how you actually take bookings. Safer: "No payment to request a quote."
- "Limited offer — Pay by Bank Transfer, Get a Discount! No card processing fees" (banner/modal): the discount terms are not in any data file.
- "₿ WE NOW ACCEPT CRYPTO · BTC · ETH · USDT" banner: confirm that you really accept it.
- Boat-party page: "ice tubs, Bluetooth speaker and standard inflatables", "12 NM coastal cruise" (not in the authoritative inclusions list).
- Six boat pages whose "from" price differs from `config/boats.json` (listed in `reports/plans/30_day_backlog.md`, H1).

## D. How to approve
Reply with: (1) "Use A and B as written" or your edits; (2) the real reply-time figure, if any; (3) the review source; (4) what to do with C. I will then change the templates, regenerate, show you the diff, and deploy once.

---
# Google Business Profile — how to check whether one exists and who owns it (no changes needed)
1. **Search on Google (not logged in to anything special):** search `Boat Rental Marbella` and `boatrentalinmarbella.com` on google.com and in Google Maps. Look for a panel on the right (desktop) or a card on top (phone) with the business name, a phone number and a "Website" button. If you see one, click **"Own this business?" / "Claim this business"** *only to read the message* (do not complete the claim). If it says it is "already verified / managed by someone", a profile exists and is owned.
2. **Check the account you normally use:** go to **business.google.com** signed in with `andra.kiirkivi@gmail.com` and with `boatrentalinmarbella@gmail.com` (use each in turn). If a profile appears in the list, you own or manage it. Open it → three-dot menu → **Business Profile settings → Managers** to see every owner and manager.
3. **Check your email:** search both inboxes for `business profile`, `Google Business`, `verification postcard` and `verify your business`; a past verification code or postcard shows an old attempt.
4. **If someone else owns it:** on the profile choose **Request access**. The current owner gets an email. If they don't answer in 3 days you can use Google's ownership-request flow. Do not create a duplicate.
5. **If none exists:** do nothing yet. Tell me, and we decide together: Google only allows a profile for a business with a real local presence and an address or service area that customers can legitimately use. We will check your eligibility first and never use a virtual address or add keywords to the name.
6. **Send me:** the profile link (or a screenshot of the search result) and the owner/manager email shown in step 2. That is all I need to continue.
