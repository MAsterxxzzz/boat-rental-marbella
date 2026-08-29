#!/usr/bin/env python3
"""Deploy 301 redirects by creating HTML redirect pages."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "site" / "blog"
REDIRECTS_CSV = ROOT / "SEO_REDIRECTS_TODO.csv"

def create_redirect_page(old_path, new_path):
    """Create an HTML redirect page at old_path that redirects to new_path."""

    # Extract slug from path (remove /blog/ prefix and trailing /)
    old_slug = old_path.replace('/blog/', '').rstrip('/')

    # Create directory if it doesn't exist
    redirect_dir = BLOG_DIR / old_slug
    redirect_dir.mkdir(parents=True, exist_ok=True)

    # Create index.html with 301 redirect
    redirect_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Redirected</title>
    <meta charset="utf-8" />
    <meta http-equiv="refresh" content="0; url={new_path}" />
    <link rel="canonical" href="{new_path}" />
</head>
<body>
    <p>This page has moved to <a href="{new_path}">{new_path}</a>.</p>
</body>
</html>
"""

    index_file = redirect_dir / "index.html"
    index_file.write_text(redirect_html)

    return redirect_dir

def main():
    print("Deploying 301 redirects...\n")

    # Read CSV
    redirects = []
    with open(REDIRECTS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            old_url = row['OLD_URL']
            new_url = row['NEW_URL']
            if old_url and new_url:
                redirects.append((old_url, new_url))

    print(f"Found {len(redirects)} redirects to deploy\n")

    # Deploy each redirect
    created = 0
    failed = 0

    for i, (old_url, new_url) in enumerate(redirects, 1):
        try:
            create_redirect_page(old_url, new_url)
            created += 1

            if i % 50 == 0:
                print(f"  [{i}/{len(redirects)}] Created redirect pages...")

        except Exception as e:
            print(f"✗ Failed to create redirect for {old_url}: {e}")
            failed += 1

    print(f"\n" + "="*80)
    print(f"DEPLOYMENT COMPLETE")
    print(f"="*80)
    print(f"\n✓ Created: {created} redirect pages")
    if failed:
        print(f"✗ Failed: {failed} redirect pages")

    print(f"\nNEXT STEPS:")
    print(f"1. Commit changes: git add site/blog/ && git commit -m 'Deploy 301 redirects'")
    print(f"2. Push to main: git push origin main")
    print(f"3. GitHub Pages will auto-deploy within 1-2 minutes")
    print(f"4. Test a redirect: curl -L https://boatrentalinmarbella.com/blog/[OLD_SLUG]/")
    print(f"5. Update sitemap and submit to Google Search Console")

if __name__ == "__main__":
    main()
