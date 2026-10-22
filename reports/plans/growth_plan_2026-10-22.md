# Boat Rental Marbella — growth plan (researched 2026-10-22)

No ranking or traffic results are promised. Evidence is labelled; assumptions are marked **[assumption]**.

## Evidence base
- **Search Console** (proxy, 2026-09-22..2026-10-19, from `reports/daily_work_log.md`): 370 impressions, 0 clicks, 85 query×page rows, positions mostly 70–97. The binding constraint is ranking, not click-through.
- **Competitors on page one** (web search 2026-10-22): marketplaces Click&Boat (https://www.clickandboat.com/us/boat-rental/spain/puerto-banús-marbella), Nautal (https://www.nautal.com/boat-rentals-marbella), Sailo, plus local operators. The Spanish query "alquiler de barco Marbella con patrón" returns Click&Boat, CheckYeti and small operators. Marketplaces win on breadth of listings, reviews and booking trust; a single operator can't match that on generic terms.
- **Google guidance**: helpful-content self-assessment (https://developers.google.com/search/docs/fundamentals/creating-helpful-content, fetched 2026-10-22) asks for first-hand experience, a clear author/"who, how, why", and warns against date-refresh tricks and content made mainly for search. Spam policies (https://developers.google.com/search/docs/essentials/spam-policies, fetched 2026-10-22) cover link spam, forum/comment link abuse and scaled content abuse; paid links need rel="nofollow"/"sponsored".
- **Site** (repo + live homepage 2026-10-22): mobile viewport present; JSON-LD for Service/AggregateOffer/FAQPage; no AggregateRating/Review markup on the homepage; 9 WhatsApp CTAs, no `tel:` link; ~170 top-level pages including 30+ boat pages; 349 redirect stubs and ~149 fabricated-year pages (pending owner approval). 877 files carry a template `<p>`/`<div>` mismatch (fix proposed, pending).
- **Outreach tracker** (read 2026-10-22): 57 prospects; majority `sent` (Puerto Banús agents, hotels, guides), 5 drafts waiting, several bounced guessed addresses (suppressed), 1 paid-placement offer declined, 0 `backlink_confirmed`. Sends are not yet producing verified links.
- **Community rules** (fetched 2026-10-22): AngloINFO Costa del Sol (https://www.angloinfo.com/forum-guidelines) bans promotion-led posts but allows a link to an affiliated site only when it directly answers the question and a plain answer would not do. Expat Exchange and Expat Arrivals prohibit business promotion in forum posts (search snippets; pages themselves returned 403 to my fetch, so unverified at source). Reddit and TripAdvisor pages could not be fetched, so their rules are **unverified**.

## Five best opportunities (ranked)
1. **Win the Spanish-language "con patrón" intent** (impact high, effort low, risk low). `/es/` already gets impressions for "alquiler de barco con patrón marbella" (16 impr, pos ~78). Today's edit added the phrase; next is a measured follow-up: dedicated ES FAQ/section answering price-includes, licence, cancellation — only from facts already on the English pages. Measure impressions for the query cluster weekly.
2. **Convert the traffic that does arrive** (impact high, effort low–medium, risk low–medium). Zero `tel:` link, WhatsApp-only booking. Candidates: a sticky mobile WhatsApp bar, a price-and-inclusions summary above the fold, a visible "what's included / cancellation" link. Any change to booking UI is *booking functionality*, so it needs owner approval before it is built.
3. **Reviews and trust markup** (impact medium–high, effort low, risk medium). The homepage shows "Happy customers on the water" but has no Review/AggregateRating markup. Only add markup for reviews the owner confirms are real and visible; never invent ratings. Needs owner-supplied review source.
4. **Free, rule-compliant listings** (impact medium, effort medium, risk low). Candidates to verify: AngloINFO Costa del Sol business directory ("Yacht Charters & Boat Hire" category — free vs paid and account needs **unverified**), Google Business Profile status (owner-only; unverified), Bing Places, tourism-board and marina directories. Each needs an owner-held account.
5. **Fix the sitewide template flaw and clean the duplicate/fabricated-year pages** (impact medium, effort medium, risk medium). Already proposed; pending approval. Reduces crawl waste and thin-page signals.
Lower priority: forum answers. The communities found restrict promotion; value is mostly reputation, rarely a link. Do only where rules allow and a real, unanswered question exists.

## 30-day operating rotation for the existing daily routine
- Mon: on-site (one page, evidence-backed snippet/internal link/FAQ). Tue: off-site research or listing (one verified item, logged draft/submitted/live). Wed: conversion proposal or review of last week's change. Thu: on-site again, different page cluster. Fri: verify placements (fetch each submitted link; mark live only if confirmed) and weekly metrics. Sat/Sun: light — rule-checked community answer drafts or a no-change record.
- Week 1: finish ES/EN intent tweaks (done today for `/` and `/es/`); get owner decisions on items 2–3 and 5; confirm Google Business Profile ownership.
- Week 2: top 3 pages by impressions get a FAQ/snippet review; owner-supplied reviews → markup.
- Week 3: submit 2–3 free listings that need no payment/reciprocal link; start rule-checked answers where an unanswered, relevant question exists.
- Week 4: re-measure; keep what moved, drop what did not. Do not re-edit a page within 14 days without new evidence.
- Outreach: stays with the shared tracker and the 2/day combined cap; prefer prospects with a concrete gap on their page; track replies and verify any claimed link before `backlink_confirmed`.

## Weekly measurement
Search Console (same 28-day, T-3 window): relevant impressions and clicks for the boat/yacht rental query cluster in EN and ES, average position of the top 10 queries; WhatsApp enquiries and bookings (owner-reported — **not measurable from here**; ask the owner for a weekly count); outreach funnel (sent / replied / link promised / link verified); placements by status draft/submitted/live with source URL and check date.

## Not done / needs the owner
Booking-UI changes, review markup, Google Business Profile, any account creation, paid placements (declined), bulk template and future-dated page changes.
