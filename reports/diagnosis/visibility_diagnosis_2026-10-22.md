# Google visibility diagnosis — boatrentalinmarbella.com (2026-10-22)
Sources: Search Console API (property `sc-domain:boatrentalinmarbella.com`, read-only, siteFullUser), URL Inspection API, live HTTP checks, repository. Windows: current 2026-09-22..10-19, previous 2026-08-25..09-21 (28 days each, ending 3 days before today).

## 1. Search Console: current vs previous 28 days
| | Clicks | Impressions | CTR | Avg position |
|---|---|---|---|---|
| Current | 0 | 395 | 0% | 79.0 |
| Previous | 1 | 457 | 0.2% | 78.2 |
- Flat-to-slightly-down. Mobile impressions fell 144 → 87; desktop flat (313 → 308). 217 of the current impressions are from Spain, 42 from the UK.
- **Branded searches: zero** in both periods (no query containing the brand/domain). Google has essentially no brand signal for this site yet.
- Commercial terms sit around position 79–90: "boat rental marbella" 26 impr (pos 79.5, prev 16), "rent a boat marbella" 19 (79.3), "rent yacht marbella" 16 (87), "yacht charter marbella" 6 (89.5, prev 4/97). Spanish "alquiler de barco con patrón marbella" 16 impr (pos 78) is new this period.
- Pages: `/` 146 impr, `/es/` 134, `/boat-party-marbella/` 66, then a long tail. `/yacht-charter-marbella/` fell 41 → 11. Comparison pages and future-year URLs: 1 comparison page with impressions (12), **0 future-year URLs with any impressions**.
- Daily series in the API starts 2026-08-29 (impressions 89 → 196 → ... → 157): the site entered results only recently. Position ~79 is page 8.

## 2. Index status (URL Inspection API)
Core pages: `/`, `/es/`, `/yacht-charter-marbella/`, `/boat-party-marbella/`, `/catamaran-rental-marbella/`, `/boats/astondoa-40/`, `/es/alquiler-de-yates-marbella/`, `/fr/`, `/blog/` = **Submitted and indexed**, self-canonical, robots allowed. Last crawl dates: `/` 2026-10-06, others 2026-09-11..10-10, `/blog/` 2026-07-22.
**Not known to Google at all** (never crawled): `/boats/`, `/boats/azimut-39/`, `/boat-rental-puerto-banus/`, `/de/`, `/uk/`, `/boat-rental-with-skipper/`.
Sample of 32 sitemap URLs from blog/experiences: 4 indexed, 6 "Crawled – currently not indexed", **22 unknown to Google** (all 8 sampled future-year URLs unknown).
Mobile-usability verdict is not returned by the API any more (VERDICT_UNSPECIFIED) — not checked via Google; the page has a viewport meta tag.

## 3. Technical checks (live)
OK: `http://`, `www` and non-www all 301/redirect to `https://boatrentalinmarbella.com/` (1 hop); `/boats` → `/boats/`. robots.txt allows all and lists 3 sitemaps. All key pages return 200 with self-canonical and no noindex. Homepage hreflang lists 11 languages + x-default, reciprocal checks pass (0 issues). JSON-LD present (Service, AggregateOffer, FAQPage, BreadcrumbList). Crawl check: 0 broken internal links across 57,948 links; 801 sitemap URLs, 0 missing.
Problems: (a) `sitemap.xml` lists 800 URLs, **every `lastmod` is 2026-07-18/08/21/22** though pages were edited since; (b) 626 of 800 sitemap URLs are blog (439) and experiences (187) pages, of which 219 have future years in the URL; (c) `/boat-rental-with-skipper/` was missing from the sitemap (**fixed, see below**); (d) 349 redirect stubs use `<meta refresh>` + HTTP 200 (soft redirects, GitHub Pages cannot send 301) — none are in the sitemap; (e) GSC's sitemaps list returned no entries for this service account, so submitted/indexed sitemap counts are **unverified**.

## 4. Content quality (blog)
- 880 blog folders: 349 redirect stubs, **531 real pages**; 522 carry datePublished 2026-05 (one bulk batch), none dated in the future. **98 real blog pages have a year after 2026 in the URL/title** (2027–2052) while their stated publication date is 2026-05-16 — years are invented, not events. 91 boat-comparison pages (15 with future years). Comparison pages are not textual near-duplicates (6-gram overlap median 0.14, max 0.19) but share one template; median length 1,344 words.
- Google's view: of the 32 sampled, most are never crawled or crawled-not-indexed; future-year URLs earn 0 impressions.
- Authoritative-data check of the homepage: fleet "29-boat" matches `config/boats.json` (29); "From €749 / 2h" matches `price_anchor_low_2h` 749; review claim "4.9-star average ... verified reviews" matches `config/reviews.json` aggregate 4.9 from 20 curated reviews, **but the file calls them "curated", so "verified" is not supported by the data**; the homepage has no AggregateRating markup (correct — it is only on `/reviews/`). **Response-time claims ("WhatsApp reply in <5 min", "within 5 minutes") are not in any authoritative data file** — owner must confirm or they should be softened.

## 5. Diagnosis
Not a technical block: robots, canonicals, redirects and hreflang are sound, and the core pages that Google has crawled are indexed. The problem is **authority/crawl demand**: a very new site (impressions from late Aug) with no brand searches, ranking ~page 8 for its head terms, and a sitemap where ~78% of URLs are low-priority blog/experience pages (219 with invented future years) that Google mostly has not crawled. Key money pages (`/boats/`, `/boats/azimut-39/`, `/boat-rental-puerto-banus/`) are not yet known to Google. More pages will not help; fewer, stronger, discoverable pages and real off-site signals will.

## 6. What was changed
One narrow fix (see work log): added `/boat-rental-with-skipper/` to `site/sitemap.xml`. It does not guarantee indexing.

## 7. URL-level recommendations
`url_recommendations_2026-10-22.csv` (724 live blog+experience pages): 191 are future-year URLs → **pending approval**, handled by the existing plan (not altered); 533 → keep-and-improve (fact-check, dedupe within comparison families, add unique content). **No bulk delete, redirect, noindex or rewrite is proposed or done.** Suggested next step for approval: shrink the sitemap to money pages + best-performing guides (decision for owner).

## 8. Owner decisions needed
Confirm or soften the "<5 min reply" and "verified reviews" claims; approve (or not) removing future-year URLs from the sitemap; Google Business Profile status; weekly enquiry/booking counts.
