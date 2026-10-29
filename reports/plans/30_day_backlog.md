# 30-day execution backlog (from 2026-10-22) — read this each routine run
Rules: one completed, verified action per run. A draft, report or unverified submission is **not** completed work. Do not re-edit a page within 14 days without new evidence. Pending-approval items stay pending. Status values: todo / done(proof) / blocked(reason).

## A. Owner-only prerequisites (unblock the rest)
- A1 Confirm or soften "WhatsApp reply in <5 min / quote within 5 minutes" (homepage, blog hub, booking modal): no authoritative data supports it. blocked: owner.
- A2 Confirm "verified reviews" wording vs `config/reviews.json` ("curated"); supply the real review source (Google/Click&Boat/WhatsApp screenshots) so wording can be accurate. blocked: owner.
- A3 Google Business Profile: owner confirms whether one exists (no Maps link on site, none found by web search). Eligibility is the owner's to confirm: a real, staffed local presence or a genuine service-area business with accurate address policy; phone on site is +358 (Finland) so a local contact number may be needed. Never create a second profile, use a virtual/fake address, add keywords to the name, or ask for incentivised/fake reviews. blocked: owner.
- A4 Decide the sitemap policy: shrink to money pages + best guides (recommended), keep future-dated pages out of it. blocked: owner approval.
- A5 Approve/decline the future-dated pages plan and the footer `</p>` rollout (pending since 2026-10-02).

## B. Existing-page improvements (one per run, evidence from GSC)
- B1 /yacht-charter-marbella/: DONE 2026-10-22 (title/H1 'from €450' → 'from €749', matches data). Next: measure after 14 days; FAQ addition only after that.
- B2 /boats/ and /boats/azimut-39/, /boat-rental-puerto-banus/, /de/, /uk/ are unknown to Google: add contextual internal links from indexed pages (/, /es/, /yacht-charter-marbella/), then request indexing in Search Console (owner/GSC UI). todo
- B3 /es/ and /es/alquiler-de-yates-marbella/ (indexed; pos 53 on one query): confirm "con patrón" wording is mirrored in titles/H1 after the 2026-10-22 edit; measure before touching. todo (measure first, not before 2026-11-05)
- B4 /boat-party-marbella/: DONE 2026-10-22 (460e5cb7): unsupported catamaran/40-guest boats and prices replaced with fleet-verified facts. Next: measure; consider a snippet tweak after 14 days.
- B5 Re-link strategy for the blog hub: it links 349 redirect stubs and 98 future-year pages (51% of 871 links). Removing those cards is a bulk change → needs approval (A4/A5).
- Done: sitemap now lists /boat-rental-with-skipper/ (2080baec); blog hub claim corrected 887→522 (e37f6c7f); homepage yacht link (f24d06c); /es/ con patrón (d4e6942).

## C. Authentic customer proof
- C1 After A2: add accurate review excerpts + AggregateRating markup only on pages that visibly show the reviews (Google requires the count to match). todo
- C2 Add a short, honest "how we respond" line only once the real response time is confirmed (A1). todo

## D. Eligible local visibility (free, rule-compliant, owner accounts)
- D1 Google Business Profile (after A3). D2 Bing Places. D3 AngloINFO Costa del Sol business directory ("Yacht Charters & Boat Hire") — check whether a free listing exists. D4 Marbella/Puerto Banús marina and tourism directories that list charter operators without payment or reciprocal links. Each: record URL, status draft/submitted/live, check date. blocked: needs owner accounts.

## E. Partner / editorial mentions
- E1 Follow up on replies in the Outreach Tracker (Simply Shuttles positive reply, DM Properties acknowledgment); verify any claimed link on the live page before `backlink_confirmed`. 0 confirmed so far.
- E2 Outreach stays with the shared tracker and the 2-per-day combined cap; prefer pages with a concrete gap (e.g. guides that mention yachts without naming a charter operator). Never contact the same address twice.

## F. Useful non-spam promotion
- F1 Answer real, unanswered questions only where rules allow (AngloINFO: affiliated link only if it directly answers the question; owner account needed). Draft first in reports/offsite_drafts/; post only from an owner account.

## G. Weekly measurement (Fridays)
GSC 28-day vs previous 28-day (end = today−3): clicks, impressions, avg position for non-branded commercial queries (EN/ES), brand queries (currently 0), index status of the 6 unknown core pages, verified live placements, enquiries/bookings (owner-reported).

## H. Owner decisions found 2026-10-22
- H1 Price conflict: 6 boat pages show a 'from' price different from config/boats.json (Sunseeker Predator 72: 5,000 vs 4,200; Princess F70: 3,799/2h vs 3,500/4h; Sunseeker 68 Sport: 6,500 vs 3,600; Sunseeker 63: 1,999/2h vs 3,200/4h; Princess V58: 2,999 vs 2,400; Sunseeker Predator 58: 2,999 vs 2,800). Owner states the correct prices; then fix the wrong side. blocked: owner.
- H2 80 real pages dated 2027-2029 are not covered by the future-dated proposal (see reports/diagnosis/future_dated_reconciliation_2026-10-22.md). blocked: owner.
- H3 Boat-party page still says 'Prices include ... ice tubs, Bluetooth speaker and standard inflatables' and '12 NM cruise'; not in the authoritative inclusions list. Confirm or remove. blocked: owner.

- H4 Claims wording (A/B/C in reports/proposals/claims_wording_for_approval_2026-10-22.md): awaiting owner approval; template change affects 862 pages (bulk).
- A3 update: owner is unsure whether a Google Business Profile exists; steps to check are in the same proposal file. Do not create or modify any profile.

- B6 DONE 2026-10-22 (a33d2e51): /sunset-cruise-marbella/ title/H1 'from €250'→'from €749', 3h cruise €350→€1,049 (data: tier_a). Scan of all page titles vs descriptions found 1 more mismatch: /jet-ski-rental-marbella/ title 'from €200/h' vs description '€250' (data: Sea-Doo 1h €250; €200 appears only as additional-hour rate per llms text) - owner to confirm wording.
- B7 NEXT: /catamaran-rental-marbella/ (indexed) title says 'Sail & Power Catamarans from €350'; boats.json has one catamaran (Lagoon 380, 'on request', no price). Verify with owner or soften to 'quote on WhatsApp' before editing.

- B8 DONE 2026-10-22 (e186645e): /boat-rental-puerto-banus/ (target for 'boat hire Puerto Banús'; unknown to Google) - 'starts at €250' → €749 and the generic market price table (motor yacht 10-12 m 2h €275, 40 ft catamaran, 25 m+ superyacht) replaced by fleet-verified rows. STILL UNVERIFIED on that page (owner): 'roughly 60% of inventory berths here', Pier 3/pier-by-boat table, overnight '€1,200 a night' FAQ, 'catamarans 38-55 ft' FAQ.
- NEXT (independent of owner): B2 - add 1-2 contextual internal links to the pages Google does not know (/boats/azimut-39/, /boat-rental-with-skipper/ already in sitemap) from pages already indexed and not edited in the last 14 days (e.g. /catamaran-rental-marbella/ body, /boat-rental-4-hours/), then re-inspect index status; and fact-check /private-boat-charter-marbella/ and /es/alquiler-de-yates-marbella/.

- B9 DONE 2026-10-22 (53049ee4): /catamaran-rental-marbella/ title 'from €350' → 'Price on Request' (owner: on request). Body price guide not touched (owner decision).
- B10 DONE 2026-10-22 (5514da49): /nl/ title/meta/H1 'Boot huren Marbella' (GSC: boot huren marbella pos 65) + stale featured cards fixed. 8 other language hubs have the same stale cards (Mangusta 80 '€2299/2h', Canados 86 '€2099/2h', 10 pax): awaiting approval to regenerate/patch (careful: regeneration strips gtag/ai-graph/analytics scripts - patch surgically).
- B11 SCHEDULED after 2026-11-05 (14-day rule): add 'boat hire' wording to homepage and /uk/; measure /es/ 'con patrón' effect; see reports/plans/keyword_to_page_map_2026-10-22.md.

- B2 PARTIAL DONE 2026-10-22 (096ebc48): /boat-rental-4-hours/ now links /boat-rental-puerto-banus/ and /boats/azimut-39/ (both unknown to Google). Deploy success, live verified. NEXT: same for /boats/ (hub) and /de/, /uk/ from indexed pages not edited in 14 days; owner to request indexing in Search Console UI.

## I. Google Business Profile (2026-10-22)
- I1 DONE: profile verified (SMS), hours/categories/services/logo/photos submitted; review kit created (see reports/plans/gbp_reviews_playbook.md).
- I2 blocked: wait until the profile is public (owner confirms), then add the review link to /reviews/ and the profile URL to sameAs. Do NOT add before it is public.
- I3 owner: collect first real reviews with the QR card / WhatsApp message (no incentives).

- B12 DONE 2026-10-26 (33cdc92): /blog/puerto-banus-vs-marbella-marina/ fact-fixed (departure port) + link to /boat-rental-puerto-banus/. NEXT: fact-check /es/alquiler-yate-celebraciones-marbella/ and /experiences/ pages.
- B2 PARTIAL DONE 2026-10-24 (c2cb2b8): /boat-rental-prices/ (last edit 10-04) now links /boat-rental-puerto-banus/ and /boat-rental-with-skipper/. Deploy success, live verified. /boats/ already linked sitewide (nav) so no further link work needed there; remaining: /de/, /uk/ contextual links; owner to request indexing in GSC UI. Fact-check of /es/alquiler-de-yates-marbella/: page created 10-23, recheck after 14 days.
- B13 DONE 2026-10-27 (9f52f221): /experiences/ snippet '9 ... from €200' -> '16 ... from €749 for 2 hours'; jet-ski card €200->€250. NEXT: B11 after 11-05; owner decisions on wedding-ceremony claim, Gibraltar price, multi-port departures claim.
- B14 DONE 2026-10-28 (d1ac9c56): jet-ski title 'from €200/h' -> 'from €250'.
- B15 DONE 2026-10-28 (9de8578e): Nikki Beach guide beach-club drop-off wording + Puerto Banus link. NEXT: Gibraltar day-trip blog price on request + Ceuta.
- B16 DONE 2026-10-29 (942ebb88): Gibraltar day-trip guide price -> on request.
