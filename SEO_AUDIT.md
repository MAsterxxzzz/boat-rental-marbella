# Boat Rental Marbella — SEO Audit Report
**Date:** 2026-08-29  
**Auditor:** Claude Code SEO Review  
**Current Site Status:** High-value core content with CRITICAL issue: auto-generated thin/duplicate pages

---

## EXECUTIVE SUMMARY

### ✅ What's Working Well
1. **Core business pages** (0.9+ priority in sitemap)
   - Well-structured category pages: /yacht-charter-marbella/, /boat-rental-puerto-banus/, /luxury-yacht-rental-marbella/, etc.
   - Proper internal linking hierarchy
   - Good schema markup (LocalBusiness, Service, BreadcrumbList, FAQPage)
   - Founder/author information included (Andra Kiirkivi)
   - Real pricing, capacity, and business data

2. **Boat inventory** (30 boats)
   - Individual boat pages with photos, videos, specs
   - Real fleet data, not invented
   - Proper internal linking to parent categories

3. **Experiences & occasions**
   - /experiences/ pages for specific charter types
   - Sunset, party, corporate, romantic, water sports, etc.
   - Good thematic clustering

4. **Technical foundation**
   - HTTPS, responsive design, mobile-first
   - XML sitemaps (sitemap.xml, sitemap-index.xml, sitemap-video.xml)
   - robots.txt with proper directives
   - No obvious crawl blocks
   - Google Analytics installed
   - Proper canonical tags

5. **Trust signals**
   - Real company info (Andra Kiirkivi, founder)
   - Local address (Marbella, Spain)
   - WhatsApp booking CTA
   - Clear business identity

### 🚨 CRITICAL ISSUE: Auto-Generated Thin Content
**Problem:** 887 blog posts, many of which are near-duplicate comparison pages with auto-appended year/number suffixes

**Evidence:**
```
astondoa-40-vs-azimut-39-vs-pershing-46-marbella-three-way-comparison           [canonical]
astondoa-40-vs-azimut-39-vs-pershing-46-marbella-three-way-comparison-2030      [DUPLICATE]
astondoa-40-vs-azimut-39-vs-pershing-46-marbella-three-way-comparison-2031      [DUPLICATE]
astondoa-40-vs-azimut-39-vs-pershing-46-marbella-three-way-comparison-2042      [DUPLICATE]

azimut-39-vs-fairline-targa-12m-marbella-comparison                            [canonical]
azimut-39-vs-fairline-targa-12m-marbella-comparison-2037                       [DUPLICATE]
azimut-39-vs-fairline-targa-12m-marbella-comparison-2045                       [DUPLICATE]
azimut-39-vs-fairline-targa-12m-marbella-comparison-2046                       [DUPLICATE]
```

**Impact on SEO:**
- ❌ Google treats these as thin, auto-generated content
- ❌ Massive keyword cannibalization (same intent, multiple URLs)
- ❌ Crawl budget waste (Googlebot indexes duplicates instead of unique content)
- ❌ Diluted authority (canonicals ineffective with this volume)
- ❌ Risk of manual action penalty or algorithmic suppression
- ❌ Search result fragmentation (Google may show wrong version)

**Example Search Result Risk:** User searches "astondoa 40 vs azimut 39 marbella"  
→ Google could rank the -2030, -2031, or -2042 version instead of canonical  
→ User gets older/wrong information  
→ No ranking boost across versions (authority spread thin)

---

## SITE STRUCTURE INVENTORY

### Page Count by Category
| Category | Count | Status |
|----------|-------|--------|
| Main/Navigation | ~15 | ✅ Good |
| Boat pages | 30 | ✅ Good |
| Core category pages | ~40 | ✅ Good |
| Experience pages | ~30 | ✅ Good |
| Blog posts (unique value) | ~50-80? | ⚠️ Unknown |
| Blog duplicates | ~800+ | 🚨 **CRITICAL** |
| Language versions (if all copied) | +4x multiplier | 🚨 Amplifies problem |
| **TOTAL INDEXED** | 1,256+ | 🚨 Problem |

### Blog Post Content Types Identified
1. **High-value content** (KEEP):
   - "Boat Rental Marbella Prices — Complete Guide" (if exists)
   - "Do You Need a Licence to Rent a Boat in Marbella?"
   - "What Is Included in a Marbella Boat Rental?"
   - Duration-based guides (2hr, 4hr, 8hr rentals)
   - Occasion guides (birthdays, hen parties, corporate, romantic)
   - Destination/route guides (Calas, Tarifa day trip, etc.)

2. **Thin/Duplicate Comparison Pages** (NOINDEX or CONSOLIDATE):
   - Astondoa 40 vs Azimut 39 (4 versions!)
   - Astondoa 40 vs Pershing 46 (3+ versions)
   - Azimut 39 vs Fairline Targa (4 versions with future dates!)
   - Pershing 46 vs Sunseeker (4 versions)
   - And hundreds more...

3. **Metadata Issues**:
   - Future publication dates (2037, 2042, 2046) — appears to be bug in content generation
   - All use picsum.photos for OG images (placeholder, not real boat photos)

---

## CURRENT PAGE METRICS

### Indexation Status
- **Sitemaps declared:** 3 (sitemap.xml, sitemap-index.xml, sitemap-video.xml)
- **robots.txt:** Properly configured, all crawlers allowed
- **Language versions:** EN (primary), DE, ES, PL, SV, NO (probably creates 6x multiplier)
- **Estimated indexed pages:** 1,200+

### Core Web Vitals Risk
- ✅ Mobile responsive design confirmed
- ✅ Clean semantic HTML structure
- ⚠️ JavaScript minimal (good)
- ❓ Need CWV data from GSC (Lighthouse score)

### Conversion Path Issues
- ✅ WhatsApp CTA prominent on key pages
- ✅ Clear pricing visible
- ✅ Capacity/inclusions documented
- ⚠️ Thin blog pages may not convert (low intent)

---

## KEYWORD CANNIBALIZATION MAP

### Primary Search Intents Being Diluted

**"Astondoa 40 vs Azimut 39" (4 pages competing for 1 search intent)**
```
1. astondoa-40-vs-azimut-39-marbella [canonical candidate]
2. astondoa-40-vs-azimut-39-cost-comparison
3. astondoa-40-vs-azimut-39-fuel-cost-comparison-2026
4. astondoa-40-vs-azimut-39-vs-pershing-46-... (confuses intent)
```

**"Azimut 39 vs Fairline Targa 12m" (4+ pages with future-dated duplicates)**
```
1. azimut-39-vs-fairline-targa-12m-marbella-comparison [canonical]
2. azimut-39-vs-fairline-targa-12m-marbella-comparison-2037 [DUPLICATE]
3. azimut-39-vs-fairline-targa-12m-marbella-comparison-2045 [DUPLICATE]
4. azimut-39-vs-fairline-targa-12m-marbella-comparison-2046 [DUPLICATE]
```

**Result:** Google sees fragmented, auto-generated content; ranks none highly

---

## COMPETITOR ANALYSIS OBSERVATIONS

(Assuming typical Marbella boat rental competitors rank for similar keywords)

Competitors likely have:
- ✅ Smaller page counts (100-300 pages) = better quality signal
- ✅ Focused category pages (no duplicate comparison pages)
- ✅ Real blog content (weekly articles, not auto-generated)
- ✅ Cleaner internal link profiles
- ✅ Authentic review/testimonial sections
- ❓ Better local SEO (Google Business Profile optimization)

**Boat Rental Marbella's opportunity:**
- Consolidate thin pages into 1-2 killer comparison guides
- Redirect 800+ duplicates to canonical versions
- Invest time in depth, uniqueness, and real value
- Become the most authoritative voice on Marbella boat rentals

---

## MISSING VALUABLE CONTENT

### Keyword Clusters NOT SERVED (or served by thin pages)

1. **Pricing & costs**
   - "Boat Rental Marbella Prices" (complete guide)
   - "2 Hour vs 4 Hour vs 8 Hour Charter" (value comparison)
   - "Budget Boat Rentals Marbella" (under €300)
   - "Luxury Yacht Rental Marbella Prices"
   - "Boat Rental Marbella with Skipper vs Without"

2. **Practical guides (booking intent)**
   - "How to Book a Boat in Marbella" (step-by-step)
   - "What to Bring on a Boat Trip in Marbella"
   - "Best Time of Day for a Marbella Boat Trip"
   - "Weather & Sea Conditions for Marbella Boats"
   - "Cancellation Policy Explained"

3. **Location specificity**
   - "Puerto Banús Boat Rental — Complete Guide"
   - "Boat Rental from Marbella Marina (Puerto Deportivo)"
   - "Cabopino Beach Boat Rental"
   - "Estepona Boat Rental"
   - "Boat Rental Sotogrande"

4. **Use case guides**
   - "Marbella Boat Rental for Birthdays" (depth beyond thin page)
   - "Hen Party Boat Rental Marbella" (complete guide)
   - "Corporate Team Building Boat Charter Marbella"
   - "Romantic Sunset Charter Marbella"
   - "Family Boat Trip Marbella" (with kids' tips)

5. **Logistics & trust**
   - "Do You Need a Boating License in Marbella?" (FAQ-heavy)
   - "Safety on a Marbella Boat Rental"
   - "Boat Rental Insurance Marbella"
   - "Dietary Requirements & Allergies (What We Can Accommodate)"

6. **Lifestyle & inspiration**
   - "Best Boat Trips from Puerto Banús"
   - "Hidden Calas (Bays) Around Marbella"
   - "Snorkeling Spots Accessible by Boat from Marbella"
   - "Dolphin Watching in Marbella Waters"
   - "Sunset Spots Visible from a Marbella Boat"

---

## INTERNAL LINK PROFILE

### Strengths
- ✅ Main pages link to boat categories correctly
- ✅ Category pages (experiences, boat types) properly siloed
- ✅ Breadcrumb structure in schema markup
- ✅ Navigation menu covers primary intents

### Issues
- ⚠️ Blog pages likely have weak internal linking
- ⚠️ Thin duplicate pages probably don't link to high-value categories
- ⚠️ Missed opportunities to cross-link related experiences
- ⚠️ No clear "read next" or "related" linking on blog posts

---

## STRUCTURED DATA AUDIT

### What's Implemented (✅ Good)
- LocalBusiness schema (complete with address, phone, social)
- Organization schema (proper founder/team info)
- BreadcrumbList (navigation structure)
- BlogPosting (on blog articles)
- FAQPage (excellent use on comparison pages)
- Service schema (with real pricing & offers)
- Article schema (publication dates, author)
- Person schema (Andra Kiirkivi — founder)

### Issues Found
- ⚠️ OG images use picsum.photos placeholder (should use real boat photos)
- ⚠️ Future-dated publication dates (2037, 2042, 2046) — schema errors
- ⚠️ No Review/AggregateRating (fake reviews risky, but missing genuine social proof)
- ❓ No Event schema (if offering scheduled charters, this would help)

### Missing Opportunities
- ❓ Event schema (if charter dates/times are bookable)
- ❓ VideoObject schema (for boat videos)
- ❓ Offer schema optimization (currently present, could be richer)

---

## IMAGE SEO AUDIT

### Issues
- 🚨 **Placeholder images:** Blog OG images use picsum.photos (not real boat photos)
- ⚠️ **Filenames unclear:** Likely generic (may need renaming for SEO)
- ✅ **Alt text:** Appears to be present (good)
- ✅ **Responsive sizing:** Confirmed in code
- ⚠️ **Compression:** Unknown (should check with GTmetrix)

### Needed
- Real boat photos for blog posts (Azimut 39, Astondoa 40, etc.)
- Descriptive filenames (azimut-39-deck-lounge-1200.jpg vs photo_123.jpg)
- Google Images optimization (boat model + location + activity tags)

---

## MOBILE UX ASSESSMENT

### Confirmed Good
- ✅ Responsive viewport meta tag
- ✅ Mobile-first CSS (seen in stylesheet)
- ✅ Hamburger menu for mobile nav
- ✅ Touch-friendly CTA buttons (WhatsApp, Book)
- ✅ Discount popup responsive (recent fix)
- ✅ Hero video with mobile play button (recent fix)

### To Verify (GSC/Field Data)
- Core Web Vitals (LCP, FID, CLS)
- Mobile click-through rate
- Mobile conversion rate (WhatsApp clicks)

---

## HOMEPAGE SILO STRUCTURE

**Current hierarchy:** Well-designed

```
HOME
├─ Boats (fleet inventory)
├─ Experiences (charter types)
├─ Yachts (product category)
├─ Puerto Banús (location)
├─ Blog (guides & comparisons)
└─ Contact

Boats
├─ Astondoa 40
├─ Azimut 39
├─ Azimut 58
└─ [28 others]

Experiences
├─ Champagne Sunset
├─ Booze Cruise
├─ Romantic Dinner
└─ [27 others]
```

**Assessment:** ✅ Clean silo structure, no major cannibalization at category level.  
**Problem:** ⚠️ Within blog, massive duplication breaks structure

---

## ROBOTS.TXT & CRAWL EFFICIENCY

### Current robots.txt
```
User-agent: *
Allow: /

[LLM crawlers explicitly welcomed: GPTBot, ClaudeBot, PerplexityBot, etc.]

Sitemap: https://boatrentalinmarbella.com/sitemap-index.xml
Sitemap: https://boatrentalinmarbella.com/sitemap.xml
Sitemap: https://boatrentalinmarbella.com/sitemap-video.xml
```

**Assessment:** ✅ Correct (all crawlers allowed, sitemaps declared)

### Crawl Budget Concern
- ⚠️ With 1,256 pages and 887 blog posts, Google may waste crawl budget on thin duplicates
- ⚠️ Estimated **real value:** ~120 pages, **actual crawl target:** 1,200+ pages
- ⚠️ Result: **10x crawl waste**; real content doesn't get revisited as often

---

## RECOMMENDATIONS BY PRIORITY

**See SEO_BACKLOG.md for detailed task breakdown**

### P0 — CRITICAL (Do First, High Impact)
1. **Audit exact blog post duplicates** — script to identify near-duplicate content
2. **Noindex or redirect 800+ thin pages** — consolidate to ~50 canonical comparisons
3. **Fix schema errors** — remove future dates (2037, 2045, etc.)
4. **Update OG images** — use real boat photos, not placeholders
5. **Create 1-2 killer comparison guides** — astondoa-40-vs-azimut-39 (comprehensive)

### P1 — HIGH VALUE (Quick Wins)
1. **Create missing core guides** — boat rental prices, booking how-to, FAQs
2. **Optimize existing category pages** — yacht-charter-marbella/, boat-rental-puerto-banus/
3. **Internal link audit & fixes** — ensure thin pages don't dilute authority
4. **Improve homepage** — stronger intro, clear value prop, CTA hierarchy
5. **Canonical tag audit** — ensure all duplicates properly point to canonical

### P2 — MEDIUM VALUE (Ongoing)
1. **Create location-specific guides** — Puerto Banús, Marbella Marina, Estepona, etc.
2. **Expand experience guides** — depth for birthdays, hen parties, corporate events
3. **Image optimization** — rename files, compress, add rich alt text
4. **Video schema** — optimize boat videos for search results
5. **FAQ expansion** — add more structured Q&A to top pages

### P3 — NICE TO HAVE (Future)
1. **Blog automation audit** — understand why duplicates are being created
2. **Backlink audit** — where is authority coming from?
3. **Competitor deep-dive** — detailed SERP analysis for top 10 keywords
4. **Social proof integration** — reviews, testimonials, customer photos
5. **Local SEO** — Google Business Profile optimization

---

## QUESTIONS FOR THE USER

Before implementing changes, clarify:

1. **Blog content automation:** Why is the system creating 887 blog posts with duplicate comparisons? Should this stop?
2. **Future dates:** Why do some pages have publication dates of 2037, 2042, 2046? Is this a bug?
3. **Content value:** Which of these 887 posts receive actual traffic? Do any rank?
4. **Language strategy:** Are the 887 posts copied across all 6 language versions? (DE, ES, PL, SV, NO)
5. **Canonical strategy:** Are the duplicate pages currently redirected or noindexed? Or are they all indexed?
6. **Real blog budget:** How much time/resources can be invested in high-quality blog content?
7. **Founder story:** Can we expand Andra's story for E-E-A-T (Expertise, Experience, Authority, Trustworthiness)?
8. **Customer testimonials:** Do you have real customer photos/reviews we can feature?
9. **Video library:** Are boat videos available for Video schema optimization?
10. **Backlink targets:** Any existing partnerships, press coverage, or directories we should leverage?

---

## NEXT STEPS

1. ✅ **This audit document** — read & confirm findings
2. → **Create SEO_BACKLOG.md** — detailed task breakdown with P0/P1/P2/P3 prioritization
3. → **Script to identify duplicates** — automated analysis of near-duplicate blog posts
4. → **Implement P0 fixes** — noindex/redirect thin pages, fix schema errors
5. → **Test & measure** — Google Search Console monitoring after each batch
6. → **Iterate** — tackle P1 tasks, measure impact, adjust strategy

---

**Report Complete**  
For detailed task breakdown, see: **SEO_BACKLOG.md**
