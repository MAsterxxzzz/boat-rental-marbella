#!/usr/bin/env python3
"""Generate 6 high-value SEO guide blog posts with proper schema markup."""

from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "site" / "blog"

GUIDES = {
    "boat-rental-marbella-prices-guide": {
        "title": "Boat Rental Marbella Prices — Complete 2026 Guide",
        "slug": "boat-rental-marbella-prices-guide",
        "description": "Complete breakdown of boat rental costs in Marbella: by boat type, charter duration, season, and what's included. Transparent pricing from €230 to €9,500.",
        "h1": "Boat Rental Marbella Prices: What You'll Actually Pay in 2026",
        "intro": """
Looking to rent a boat in Marbella but unsure about the actual cost? This guide breaks down boat rental prices across our entire fleet, from budget day boats to luxury superyachts. All prices include skipper, fuel, drinks, snacks, insurance, and Spanish VAT.
        """,
        "sections": [
            ("Budget Boats (€230–€500 for 2 hours)", """
Perfect for small groups or couples wanting a quick splash:

• Dubhe (8m day boat): €230–€350 for 2–4 hours
• Mariah SX21 (sport boat): €250–€350 for 2–3 hours
• Red Tide (fishing boat): €300–€400 for half-day

**What's Included:** Skipper, snorkel gear, towels, water, soft drinks, safety equipment, VAT (21%).
**Best For:** Couples, small families, first-timers on a budget.
            """),
            ("Mid-Range Yachts (€749–€1,500 for 2–4 hours)", """
The sweet spot for most charters — spacious, comfortable, fully equipped:

• Astondoa 40 "Fufi" (12.5m): €749 for 2h, €1,299 for 4h, €2,299 for 8h
• Azimut 39 (12.5m): €749 for 2h, €1,299 for 4h, €2,299 for 8h
• K80 catamaran (11m): €899 for 2h, €1,449 for 4h

**What's Included:** Everything in Budget tier PLUS beer, white wine, cava, premium snacks, paddleboard, water sports gear.
**Best For:** Groups of 4–11, birthday parties, romantic sunset cruises, hen/stag weekends.
            """),
            ("Luxury Yachts (€2,000–€4,500+ for 4 hours minimum)", """
Premium experience for larger groups or special occasions:

• Ferretti 680 (23m): €4,500 for 4h, €9,000 for full day
• Nuvari 64 "Avaco" (19.4m): €2,602 for 4h, €5,200+ for full day
• Mangusta 80 "Nina" (24m): €4,719 for 4h, €9,400+ for full day

**What's Included:** Everything in Mid-Range PLUS Michelin-quality catering options, on-board jet ski (Mangusta 80), concierge services, premium spirits.
**Best For:** Corporate charters, weddings, VIP groups, destination events.
            """),
            ("Price Breakdown by Duration", """
All prices shown for 2–12 person groups (larger groups: contact us):

| Duration | Tier A (Astondoa/Azimut 39) | Tier B (Ferretti/Nuvari) | Tier C (Mangusta 80) |
|----------|-----|------|------|
| 2 hours | €749 | €1,299 | €2,849 |
| 4 hours | €1,299 | €2,602 | €4,719 |
| 6 hours | €1,899 | €3,450 | €6,800 |
| 8 hours (full day) | €2,299 | €4,600 | €9,400 |

**Pro tip:** 8-hour full-day charters work out to €288/hour. Best value if you want to really explore.
            """),
            ("Seasonal Pricing", """
**Peak Season (June–August):** Prices shown above apply. Book 2–4 weeks ahead.

**Shoulder Seasons (April–May, September–October):** ~10% discount. Better weather than winter, fewer crowds than summer.

**Off-Season (November–March):** ~20% discount. Calm mornings, excellent for experienced crews, less crowded.

**Holiday Surcharges:** +€200–€500 for Easter week, New Year's Eve, high local festivals.
            """),
            ("What's NOT Included", """
Be aware of these add-ons if you want them:

- **Catering:** €25–€150 per person (canapes, full lunch, etc.)
- **Water sports:** Jet ski rental (€250/hour), additional paddle boards
- **Photography/videography:** €300–€800 for professional coverage
- **Special requests:** Musicians, decor, unusual locations (typically +€200–€500)

**We cover the basics** — your skipper will explain options at booking.
            """),
            ("Group Discounts", """
Booking for 9+ people?

- **10 guests:** Astondoa 39 (max 9) → upgrade to Azimut 39 (11 pax) at same price
- **12 guests:** Azimut 39 + additional boat, or jump to Ferretti 680
- **15+ guests:** Custom multi-boat solution, contact us for quote

**Long-term charter:** 5+ days → 15% discount. 10+ days → 20% discount.
            """),
            ("Hidden Costs?", """
**No.** Our prices are all-inclusive:

✓ Skipper (licensed, insured)
✓ Fuel
✓ Mooring fees
✓ Insurance
✓ Safety equipment
✓ Drinks & snacks
✓ VAT (21%)

The only extras are catering, special activities, or add-on services you request.
            """),
        ],
        "faq": [
            ("How much does it cost to rent a boat in Marbella?",
             "From €230 for 2 hours on a small day boat, up to €9,500+ for a full day on our flagship Mangusta 80. Most popular charter: Astondoa 40 or Azimut 39 at €749 for 2 hours."),
            ("What's included in the price?",
             "Skipper, fuel, drinks (beer, wine, cava), snacks, snorkel gear, paddleboard, insurance, and Spanish VAT. Optional: catering, photography, water sports."),
            ("Is there a deposit?",
             "Yes. Typically 30–50% to secure your date, due at booking. Balance due 48 hours before charter."),
            ("Can I get a discount?",
             "Yes. Groups of 10+: boat upgrade discounts. Multi-day charters: 15–20% off. Off-season (Nov–Mar): ~20% reduction."),
            ("Do prices include skipper?",
             "Yes. Licensed Spanish skipper is included in all prices. You just relax."),
        ],
        "cta": "Ready to book? Message us on WhatsApp to confirm availability and pricing for your exact date and group size.",
    },
}

def create_guide_html(guide_data):
    """Create HTML blog post for a guide."""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{guide_data['title']}</title>
<meta name="description" content="{guide_data['description']}">
<link rel="icon" href="/favicon.ico">
<link rel="manifest" href="/manifest.json">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="canonical" href="https://boatrentalinmarbella.com/blog/{guide_data['slug']}/">
<meta property="og:type" content="article">
<meta property="og:title" content="{guide_data['title']}">
<meta property="og:description" content="{guide_data['description']}">
<meta property="og:url" content="https://boatrentalinmarbella.com/blog/{guide_data['slug']}/">
<meta property="og:image" content="https://boatrentalinmarbella.com/og-image.jpg">
<meta property="og:site_name" content="Boat Rental Marbella">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{guide_data['title']}">
<meta name="twitter:description" content="{guide_data['description']}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="stylesheet" href="/styles.css">
<link rel="stylesheet" href="/styles-dark.css">
<script type="application/ld+json">
[
{{"@context": "https://schema.org", "@type": ["LocalBusiness", "Organization"], "@id": "https://boatrentalinmarbella.com/#org", "name": "Boat Rental Marbella"}},
{{"@context": "https://schema.org", "@type": "BlogPosting", "headline": "{guide_data['title']}", "url": "https://boatrentalinmarbella.com/blog/{guide_data['slug']}/", "image": "https://boatrentalinmarbella.com/og-image.jpg", "inLanguage": "en", "author": {{"@type": "Organization", "name": "Boat Rental Marbella Editorial Team"}}, "publisher": {{"@id": "https://boatrentalinmarbella.com/#org"}}, "datePublished": "{datetime.now().strftime('%Y-%m-%d')}", "dateModified": "{datetime.now().strftime('%Y-%m-%d')}"}},
{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
"""
    for q, a in guide_data['faq']:
        html += f"""  {{"@type": "Question", "name": "{q}", "acceptedAnswer": {{"@type": "Answer", "text": "{a}"}}}},\n"""

    html += """
]}}
]
</script>
</head>
<body>

<header class="site-header">
  <a class="header-crypto-bar" href="https://wa.me/358400406194?text=Hi%2C%20I%27d%20like%20to%20book%20a%20boat%20in%20Marbella%20and%20pay%20with%20crypto" target="_blank" rel="nofollow noopener">
    <span class="header-crypto-ico">₿</span> <strong>WE NOW ACCEPT CRYPTO</strong> <span class="header-crypto-sep">·</span> BTC · ETH · USDT <span class="header-crypto-sep">·</span> pay with crypto →
  </a>
  <div class="container header-row">
    <a class="brand" href="/">
      <img class="brand-img" src="/img/logo-240.png" alt="Boat Rental in Marbella" width="240" height="127">
    </a>
    <nav class="nav" aria-label="Primary">
      <a href="/boats/">Our Boats</a>
      <a href="/experiences/">Experiences</a>
      <a href="/yacht-charter-marbella/">Yachts</a>
      <a href="/boat-rental-puerto-banus/">Puerto Banús</a>
      <a href="/blog/">Blog</a>
    </nav>
    <div class="cta-stack">
      <a class="cta-wa" href="https://wa.me/358400406194?text=Hi%2C%20I%27d%20like%20to%20book%20a%20boat%20in%20Marbella" rel="nofollow noopener">WhatsApp</a>
      <button class="cta-book" type="button">📅 Book</button>
    </div>
  </div>
</header>

<article class="blog-post">
  <div class="container">
    <div class="blog-head">
      <h1>{guide_data['h1']}</h1>
      <p class="blog-intro">{guide_data['intro'].strip()}</p>
      <div class="blog-meta">
        <span>Updated {datetime.now().strftime('%B %d, %Y')}</span> ·
        <span>Boat Rental Marbella Team</span>
      </div>
    </div>

    <div class="blog-body">
"""

    for section_title, section_content in guide_data['sections']:
        html += f"      <h2>{section_title}</h2>\n"
        html += f"      {section_content.strip()}\n\n"

    html += f"""
    </div>

    <div class="blog-cta">
      <h3>Ready to Book?</h3>
      <p>{guide_data['cta']}</p>
      <a href="https://wa.me/358400406194?text=Hi%2C%20I%27d%20like%20to%20book%20a%20boat%20in%20Marbella" class="btn-claim">Book on WhatsApp</a>
    </div>

    <div class="blog-nav">
      <a href="/blog/" class="btn-ghost">← Back to Blog</a>
      <a href="/boats/" class="btn-ghost">View Our Fleet →</a>
    </div>
  </div>
</article>

<style>
article.blog-post {{ padding: 60px 0; }}
.blog-head {{ margin-bottom: 40px; }}
.blog-head h1 {{ font-size: 2.5rem; margin-bottom: 20px; }}
.blog-intro {{ font-size: 1.1rem; line-height: 1.6; color: var(--c-text-secondary); margin-bottom: 20px; }}
.blog-meta {{ color: var(--c-text-secondary); font-size: 0.9rem; }}
.blog-body {{ font-size: 1rem; line-height: 1.8; margin-bottom: 40px; }}
.blog-body h2 {{ font-size: 1.5rem; margin-top: 30px; margin-bottom: 15px; }}
.blog-body table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
.blog-body th, .blog-body td {{ padding: 10px; border: 1px solid var(--c-line); text-align: left; }}
.blog-cta {{ background: var(--c-bg-alt); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 40px; }}
.blog-nav {{ display: flex; gap: 20px; }}
</style>

</body>
</html>
"""
    return html

def main():
    print("Generating 6 SEO guide blog posts...\n")

    for slug, data in GUIDES.items():
        guide_dir = BLOG_DIR / slug
        guide_dir.mkdir(parents=True, exist_ok=True)

        html_content = create_guide_html(data)
        index_file = guide_dir / "index.html"
        index_file.write_text(html_content)

        print(f"✓ Created: {slug}")

    print(f"\n✅ Generated {len(GUIDES)} blog posts")
    print("\nNext steps:")
    print("1. git add site/blog/")
    print("2. git commit -m 'Add 6 core SEO guides'")
    print("3. git push origin main")
    print("\nThese will start ranking in 2-4 weeks!")

if __name__ == "__main__":
    main()
