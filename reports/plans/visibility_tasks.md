# Visibility task list (saved 2026-10-23)  — M = Claude does it, O = owner only (login/real activity), A = needs owner approval

## Recurring
- M: every 2-3 days re-run the 6-page index check (boats, azimut-39, puerto-banus, with-skipper, uk, de) via URL Inspection API; log result in reports/daily_work_log.md.
- M: search "Boat Rental Marbella" signed out; record whether the Business Profile appears (not yet as of 2026-10-23).
- O: after every trip send the Google review message / QR card (review_kit). Target 10 honest reviews in 30 days. No incentives, no screening.
- M (on request or local task): GBP post from reports/growth_kit/4_gbp_post_bank.md, Tue/Thu/Sat, via Chrome as andra.kiirkivi@gmail.com.

## One-off
- O: request indexing for /boat-rental-with-skipper/ and /uk/ (done 2026-10-23); next candidates /de/ and /boats/ if still unknown after 3 days.
- O: Apple Business Connect, Bing Places, Tripadvisor, Yelp, GetYourGuide/Viator listings (logins). Text in growth_kit/1_listing_text_bank.md.
- O/M: marina, hotel, concierge outreach with growth_kit/3_partner_price_sheet.md. Max 2 outreach contacts/day in the shared tracker; never the same prospect twice; owner decides referral terms.
- M after profile is public: add "Review us on Google" button on /reviews/ and the profile URL in sameAs/footer.
- M: add price lines to the GBP services and 3-4 boat products with photo (needs a profile edit session).
- M: YouTube/Instagram titles and descriptions with location and site link (owner posts).
- A: reply-time/"verified reviews" wording (862 pages); six boat-page price conflicts; 229 future-dated pages; footer rollout; stale cards on 8 language hubs; catamaran page; Spanish phone number.
- M after 5 days if profile still not found by name: inspect profile status for a hidden suspension/verification issue.

## Content queue (saved 2026-10-23; owner said "go ahead")
Cadence: 1 page per week, not daily (site already has ~880 pages; core pages still unindexed; extra thin pages dilute). Start once /boats/ and /boat-rental-puerto-banus/ leave "unknown/crawled-not-indexed" or by 2026-10-30, whichever first. Each page: new gap only (check site/ and site/es for overlap first), built from an existing page as template (head, JSON-LD, analytics, hreflang), facts only from config/boats.json, real photos from /img/boats/, one internal link to the matching money page, added to sitemap + IndexNow, one commit per page, then URL-inspection check after 3 days.
Queue (gaps from GSC queries, last 28 days):
1. ES: "Alquiler de yates para bodas, pedidas y celebraciones en Marbella" (query: alquiler de yates para bodas marbella; no ES page exists). No claims about legal at-sea ceremonies.
2. ES: "Alquiler de barco por horas en Marbella: precios 2h/4h/8h" (alquiler barco marbella por horas; check overlap with /es/ and boat-rental-prices first).
3. EN: "Best boat party in Marbella: how a private boat party works from Puerto Banús" (best boat party in marbella, boat party in puerto banus; compare with /boat-party-marbella/ first, improve that page instead if overlap).
4. ES: "Alquiler de lancha en Marbella" (alquiler lancha marbella).
5. NL: "Boot huren in Marbella met schipper" guide (boot huren marbella).
Known issue to flag to owner: existing blog posts use random picsum.photos stock images as hero/og:image, not real boats. Replace with real photos = bulk change, needs approval.
Do NOT: mass-generate with scripts/gen_blog_post.py (DeepSeek topics include unverified claims such as dolphin watching, fishing, weddings at sea).
