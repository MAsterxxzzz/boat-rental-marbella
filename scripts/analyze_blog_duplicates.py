#!/usr/bin/env python3
"""Analyze blog post duplicates and near-duplicates to identify consolidation targets."""

import json
import os
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
import re

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "site" / "blog"

def get_blog_posts():
    """List all blog post directories."""
    posts = []
    for item in BLOG_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            posts.append(item)
    return sorted(posts)

def extract_boat_names(slug):
    """Extract boat names from slug (e.g., 'astondoa-40', 'azimut-39')."""
    # Remove common suffixes
    clean = slug.replace('-marbella', '').replace('-comparison', '').replace('-2026', '')
    for year in range(2000, 2100):
        clean = clean.replace(f'-{year}', '')

    # Extract boat model patterns
    boats = re.findall(r'(astondoa-\d+|azimut-\d+|fairline-[a-z0-9-]+|pershing-\d+|mangusta-\d+|sunseeker-[a-z0-9-]+|ferretti-\d+|nuvar-\d+|canados-\d+|princess-[a-z0-9-]+|mariah-[a-z0-9-]+|bandido|dubhe|lagoon-\d+|k80|mefasa-\d+|maiora-\d+|speedboat|red-tide-[a-z-]*|sea-doo-[a-z-]*)', slug)
    return sorted(set(boats))

def get_canonical_version(similar_slugs):
    """Determine which slug should be canonical (shortest, no date suffix)."""
    # Remove date/number suffixes
    base_versions = {}
    for slug in similar_slugs:
        base = re.sub(r'-(\d{4}|\d+)$', '', slug)
        if base not in base_versions:
            base_versions[base] = []
        base_versions[base].append(slug)

    # Pick shortest base as canonical
    if base_versions:
        canonical_base = min(base_versions.keys(), key=len)
        # Return the shortest variant of canonical base
        return min(base_versions[canonical_base], key=len)
    return similar_slugs[0]

def main():
    posts = get_blog_posts()
    print(f"Found {len(posts)} blog posts\n")

    # Group by comparison type
    comparison_groups = defaultdict(list)

    for post_dir in posts:
        slug = post_dir.name
        boats = extract_boat_names(slug)

        if len(boats) >= 2:
            # This is a comparison post
            boat_key = tuple(sorted(boats))
            comparison_groups[boat_key].append(slug)

    # Analyze duplicates
    print("=" * 80)
    print("DUPLICATE COMPARISON GROUPS")
    print("=" * 80)

    duplicates = {k: v for k, v in comparison_groups.items() if len(v) > 1}
    unique_comparisons = {k: v for k, v in comparison_groups.items() if len(v) == 1}
    non_comparisons = len(posts) - sum(len(v) for v in comparison_groups.values())

    print(f"\nTotal blog posts: {len(posts)}")
    print(f"Comparison posts: {sum(len(v) for v in comparison_groups.values())}")
    print(f"  - Unique comparisons: {len(unique_comparisons)}")
    print(f"  - Duplicate comparison sets: {len(duplicates)}")
    print(f"Non-comparison posts: {non_comparisons}")
    print()

    # Show largest duplicate sets
    print("=" * 80)
    print("TOP 20 DUPLICATE COMPARISON SETS (BY COUNT)")
    print("=" * 80)

    sorted_dupes = sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)

    total_duplicates = 0
    for i, (boats, slugs) in enumerate(sorted_dupes[:20], 1):
        canonical = get_canonical_version(slugs)
        duplicates_for_this = len(slugs) - 1
        total_duplicates += duplicates_for_this

        print(f"\n{i}. {' vs '.join(boats)}")
        print(f"   Count: {len(slugs)} versions ({duplicates_for_this} to consolidate)")
        print(f"   Canonical: {canonical}")
        print(f"   Variants to redirect/noindex:")
        for slug in sorted(slugs):
            if slug != canonical:
                print(f"     → {slug}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    total_dupes_identified = sum(len(v) - 1 for v in duplicates.values())
    print(f"\nDuplicate comparison pages identified: {total_dupes_identified}")
    print(f"Unique high-value comparisons to keep: {len(unique_comparisons)}")
    print(f"Non-comparison blog posts: {non_comparisons}")
    print(f"\nEstimated indexable pages after cleanup:")
    print(f"  Current: {len(posts)}")
    print(f"  After P0-2: {non_comparisons + len(unique_comparisons) + len(duplicates)}")
    print(f"  Reduction: {total_dupes_identified} pages (~{100*total_dupes_identified/len(posts):.0f}%)")

    # Check for future dates and errors
    print("\n" + "=" * 80)
    print("SCHEMA/METADATA ERRORS SAMPLE CHECK")
    print("=" * 80)

    future_dated = []
    for slug in [p.name for p in posts[:50]]:  # Sample 50
        if re.search(r'(203\d|204\d)', slug):
            future_dated.append(slug)

    if future_dated:
        print(f"\n⚠️  Future-dated slugs found (sample of {len(future_dated)}):")
        for slug in future_dated[:10]:
            print(f"  - {slug}")
        print(f"  ... and {len(future_dated)-10} more" if len(future_dated) > 10 else "")

    print("\n✓ Analysis complete. Use this data to make P0-2 decisions.")

if __name__ == "__main__":
    main()
