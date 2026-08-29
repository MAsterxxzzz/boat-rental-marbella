#!/usr/bin/env python3
"""Comprehensive analysis of all 887 blog posts to identify content types and duplicates."""

import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "site" / "blog"

def categorize_post(slug):
    """Categorize post by content type."""

    # Extract base content (remove years)
    base = re.sub(r'-20\d{2}$|-\d{4}$', '', slug)

    if 'vs' in base or '-vs-' in base:
        return 'comparison'
    elif 'best-for' in base:
        return 'boat-review-best-for'
    elif 'review' in base:
        return 'boat-review'
    elif 'weather' in base or 'temperature' in base or 'tide' in base or 'wind' in base:
        return 'seasonal-weather'
    elif 'sunset' in base:
        return 'experience-sunset'
    elif 'birthday' in base or 'party' in base or 'bach' in base or 'hen' in base or 'stag' in base:
        return 'occasion-party'
    elif 'anniversary' in base or 'proposal' in base or 'wedding' in base or 'romantic' in base:
        return 'occasion-romantic'
    elif 'corporate' in base or 'team' in base or 'business' in base:
        return 'occasion-corporate'
    elif 'family' in base or 'kids' in base:
        return 'occasion-family'
    elif 'fishing' in base:
        return 'activity-fishing'
    elif 'snorkel' in base or 'diving' in base:
        return 'activity-water-sports'
    elif 'boat-rental' in base or 'charter-departure' in base:
        return 'location-specific'
    elif 'dolphin' in base or 'wildlife' in base:
        return 'activity-wildlife'
    elif any(day in base for day in ['christmas', 'new-year', 'nye', 'easter', 'halloween', 'epiphany', 'constitution', 'copa-del-rey']):
        return 'occasion-holiday'
    elif 'paddleboard' in base or 'jet-ski' in base or 'water-sports' in base:
        return 'activity-water-sports'
    elif 'restaurant' in base or 'wine' in base or 'food' in base or 'dining' in base or 'catering' in base:
        return 'activity-dining'
    elif 'guide' in base or 'how' in base or 'tips' in base or 'license' in base or 'rules' in base:
        return 'guide-informational'
    elif 'best' in base or 'top' in base or 'must-see' in base or 'beaches' in base or 'spots' in base or 'anchorage' in base:
        return 'guide-destinations'
    else:
        return 'other'

def get_base_content(slug):
    """Get slug without year/date suffix."""
    return re.sub(r'-20\d{2}$|-\d{4}$', '', slug)

def main():
    posts = sorted([p.name for p in BLOG_DIR.iterdir() if p.is_dir() and not p.name.startswith('.')])

    print(f"Analyzing {len(posts)} blog posts...\n")

    # Categorize
    categories = defaultdict(list)
    for post in posts:
        cat = categorize_post(post)
        categories[cat].append(post)

    # Count by category
    print("=" * 80)
    print("POSTS BY CATEGORY")
    print("=" * 80)

    sorted_cats = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
    total = sum(len(v) for v in categories.values())

    for cat, posts_in_cat in sorted_cats:
        pct = 100 * len(posts_in_cat) / total
        print(f"{cat:.<50} {len(posts_in_cat):>4} ({pct:>5.1f}%)")

    # Find duplicates by base content
    print("\n" + "=" * 80)
    print("DUPLICATE CONTENT (SAME TOPIC, DIFFERENT DATES)")
    print("=" * 80)

    base_to_posts = defaultdict(list)
    for post in posts:
        base = get_base_content(post)
        base_to_posts[base].append(post)

    duplicates = {k: v for k, v in base_to_posts.items() if len(v) > 1}
    print(f"\nContent bases with multiple date variants: {len(duplicates)}")
    print(f"Total duplicate posts: {sum(len(v) - 1 for v in duplicates.values())}")

    # Show top duplicates
    top_dupes = sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)[:15]

    print("\nTOP 15 DUPLICATED CONTENT BASES:")
    for i, (base, variants) in enumerate(top_dupes, 1):
        print(f"\n{i}. {base}")
        print(f"   Variants: {len(variants)}")
        for v in sorted(variants):
            year_match = re.search(r'-20\d{2}$|-\d{4}$', v)
            year = year_match.group(0) if year_match else ''
            print(f"     • {v} {year}")

    # Assess value vs. thin content
    print("\n" + "=" * 80)
    print("CONTENT QUALITY ASSESSMENT")
    print("=" * 80)

    high_value = []
    thin_content = []

    for cat, posts_in_cat in sorted_cats:
        if cat in ['guide-informational', 'guide-destinations', 'comparison', 'boat-review']:
            high_value.extend(posts_in_cat)
        elif cat in ['seasonal-weather', 'occasion-holiday', 'location-specific', 'activity-water-sports', 'activity-dining']:
            # Borderline - value depends on depth
            high_value.extend(posts_in_cat)
        else:
            thin_content.extend(posts_in_cat)

    print(f"\nPotentially high-value content: {len(high_value)} posts")
    print(f"Potentially thin/duplicate content: {len(thin_content)} posts")

    print("\nHigh-value categories:")
    for cat in ['guide-informational', 'guide-destinations', 'comparison', 'boat-review']:
        if cat in dict(sorted_cats):
            print(f"  • {cat}: {dict(sorted_cats)[cat]} posts")

    print("\nThin/duplicate risks:")
    print(f"  • Seasonal/weather posts (many future-dated): ~{dict(sorted_cats).get('seasonal-weather', 0)} posts")
    print(f"  • Holiday/occasion posts (event-specific): ~{dict(sorted_cats).get('occasion-holiday', 0)} posts")
    print(f"  • Location + activity combinations (thin): ~{dict(sorted_cats).get('location-specific', 0)} posts")

    # Estimate cleanup
    print("\n" + "=" * 80)
    print("ESTIMATED CLEANUP")
    print("=" * 80)

    future_dated = [p for p in posts if re.search(r'20[3-9]\d', p)]
    print(f"\nFuture-dated posts (should be cleaned): {len(future_dated)}")
    print(f"Duplicate base content: {sum(len(v) - 1 for v in duplicates.values())} (keep 1, consolidate others)")
    print(f"Likely thin/low-value: {len(thin_content)} posts (review case-by-case)")

    print(f"\nConservative estimate:")
    print(f"  Keep: 100-150 high-value posts")
    print(f"  Noindex/redirect: 700+ thin/duplicate posts")
    print(f"  Result: ~300-400 indexed blog posts (vs. current 887)")

if __name__ == "__main__":
    main()
