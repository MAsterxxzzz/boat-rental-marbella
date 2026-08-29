#!/usr/bin/env python3
"""Generate 301 redirect mappings for thin/duplicate blog posts."""

import re
import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "site" / "blog"

# High-value content to KEEP (don't redirect)
KEEP_PATTERNS = [
    'guide-informational',  # Guides & how-tos
    'guide-destinations',    # Destination guides
    'boat-review',           # Individual boat reviews
    'best-for',              # "Best for" content
]

# Content to DELETE (future-dated, thin, etc.)
DELETE_PATTERNS = {
    'future_dated': r'-(20[3-9]\d|20\d{4,})',  # 2030+
    'thin_variation': r'-(2025|2026|2027|2028|2029)-',  # Year suffixes (keep base)
}

HIGH_VALUE_BASES = {
    'boat-license-rules-spain',
    'how-much-does-it-cost-to-rent-a-boat-in-marbella',
    'best-anchorages-marbella',
    'best-beaches-by-boat-marbella',
    'best-month-to-rent-a-boat-in-marbella',
    'marbella-boat-charter-skipper-tipping-guide',
    'dietary-restrictions-yacht-catering-marbella',
}

def get_base_slug(slug):
    """Extract base slug by removing year/date suffixes."""
    # Remove various year/date formats
    base = re.sub(r'-(20\d{2})(-.*)?$', '', slug)  # -2026, -2027-guide, etc.
    base = re.sub(r'-\d{4}$', '', base)             # -2026, -2027, etc.
    return base

def should_redirect(slug):
    """Determine if a post should be redirected (is a duplicate/thin page)."""

    # NEVER redirect these (high-value)
    if slug in HIGH_VALUE_BASES:
        return False

    # Check if future-dated (2030+)
    if re.search(r'-(20[3-9]\d|20\d{4,})', slug):
        return True

    # Check if year-variant (but keep 2025-2029 base versions)
    if re.search(r'-(202[5-9]|203\d|204\d|205\d)(-|$)', slug):
        base = get_base_slug(slug)
        # If the base exists as its own post, redirect the dated version
        base_path = BLOG_DIR / base
        if base_path.exists():
            return True

    return False

def find_canonical(slug, all_posts):
    """Find the canonical version for a slug."""
    base = get_base_slug(slug)

    # If base exists, that's canonical
    if (BLOG_DIR / base).exists():
        return base

    # Otherwise, find the shortest version of this base
    variants = [s for s in all_posts if get_base_slug(s) == base]
    if variants:
        # Prefer: no suffix > 2025-2029 suffix > other
        no_suffix = [s for s in variants if s == base]
        if no_suffix:
            return no_suffix[0]

        dated = [s for s in variants if re.search(r'202[5-9]', s)]
        if dated:
            return min(dated, key=len)  # Shortest variant

        return min(variants, key=len)  # Shortest available

    return slug  # Fallback

def main():
    posts = sorted([p.name for p in BLOG_DIR.iterdir() if p.is_dir() and not p.name.startswith('.')])

    print(f"Analyzing {len(posts)} posts...\n")

    redirects = {}  # old_slug → new_slug
    kept = []
    redirected = []

    for post in posts:
        if should_redirect(post):
            canonical = find_canonical(post, posts)
            redirects[post] = canonical
            redirected.append((post, canonical))
        else:
            kept.append(post)

    print(f"RESULTS:")
    print(f"  Posts to KEEP: {len(kept)}")
    print(f"  Posts to REDIRECT: {len(redirected)}")
    print(f"  Total reduction: {len(posts)} → {len(kept)} posts (~{100*(len(posts)-len(kept))/len(posts):.0f}% fewer)\n")

    # Write CSV for review
    csv_path = ROOT / "SEO_REDIRECTS_TODO.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['OLD_URL', 'NEW_URL', 'TYPE', 'REASON'])

        for old, new in sorted(redirected):
            if old == new:
                continue

            reason = ''
            if re.search(r'-(20[3-9]\d|20\d{4,})', old):
                reason = 'future-dated'
            elif re.search(r'-202[5-9]', old) and (BLOG_DIR / get_base_slug(old)).exists():
                reason = 'year-variant'
            else:
                reason = 'duplicate'

            old_url = f"/blog/{old}/"
            new_url = f"/blog/{new}/"
            writer.writerow([old_url, new_url, reason, ''])

    print(f"✓ Redirect CSV saved to: {csv_path}")
    print(f"  → Review and manually approve before deployment\n")

    # Write Apache .htaccess rules
    htaccess_path = ROOT / "seo_redirects.txt"
    with open(htaccess_path, 'w') as f:
        f.write("# Generated 301 redirects for duplicate blog posts\n")
        f.write("# Add to .htaccess or configure in server\n\n")

        for old, new in sorted(redirected):
            if old == new:
                continue
            f.write(f'Redirect 301 /blog/{old}/ /blog/{new}/\n')

    print(f"✓ .htaccess rules saved to: {htaccess_path}\n")

    # Show sample of redirects
    print("SAMPLE REDIRECTS (first 20):")
    for old, new in sorted(redirected)[:20]:
        if old != new:
            print(f"  /blog/{old}/ → /blog/{new}/")

    if len(redirected) > 20:
        print(f"  ... and {len(redirected) - 20} more redirects")

    print(f"\n✓ Full list in: {csv_path}")

if __name__ == "__main__":
    main()
