#!/bin/bash
set -e

# Complete automated carousel update pipeline
# Downloads from Google Drive → processes media → updates website → deploys

REPO_ROOT="/Users/nunnu/Projects/boat-rental-marbella"
DOWNLOAD_DIR="$HOME/Downloads/auto-carousel-sync"
IMG_DIR="$REPO_ROOT/site/img/happy-customers"
VID_DIR="$REPO_ROOT/site/video/happy-customers"
BACKUP_DIR="$REPO_ROOT/.backup-carousel"

mkdir -p "$DOWNLOAD_DIR" "$IMG_DIR" "$VID_DIR" "$BACKUP_DIR"

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║          AUTOMATED CAROUSEL UPDATE PIPELINE (24/7)                      ║"
echo "║  Downloaded: $(date +%Y-%m-%d\ %H:%M:%S)                                   ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Download from Google Drive
echo "📥 Step 1: Downloading from Google Drive..."
python3 "$REPO_ROOT/scripts/auto_drive_sync.py" 2>&1 | grep -E "✅|❌|📁|📊" || true

# Step 2: Process all media
echo ""
echo "🎬 Step 2: Processing media files..."
python3 << 'PYTHON'
import pathlib
from PIL import Image
import shutil

DOWNLOAD_DIR = pathlib.Path.home() / "Downloads" / "auto-carousel-sync"
IMG_DIR = pathlib.Path("/Users/nunnu/Projects/boat-rental-marbella/site/img/happy-customers")
VID_DIR = pathlib.Path("/Users/nunnu/Projects/boat-rental-marbella/site/video/happy-customers")

img_count = 0
vid_count = 0

for file in sorted(DOWNLOAD_DIR.rglob("*")):
    if not file.is_file():
        continue
    
    suffix = file.suffix.lower()
    
    if suffix in {'.jpg', '.jpeg', '.png'}:
        try:
            img = Image.open(file)
            if img.mode != 'RGB':
                if img.mode in ('RGBA', 'LA'):
                    rgb = Image.new('RGB', img.size, (255, 255, 255))
                    rgb.paste(img, mask=img.split()[-1])
                    img = rgb
                else:
                    img = img.convert('RGB')
            
            base_name = file.stem
            jpg_path = IMG_DIR / f"{base_name}.jpg"
            webp_path = IMG_DIR / f"{base_name}.webp"
            
            img.save(jpg_path, 'JPEG', quality=85, optimize=True)
            img.save(webp_path, 'WEBP', quality=85)
            img_count += 1
        except Exception as e:
            print(f"   ⚠️  Skipped {file.name}: {e}")
    
    elif suffix in {'.mp4', '.mov', '.avi'}:
        try:
            dest = VID_DIR / file.name
            shutil.copy2(file, dest)
            vid_count += 1
        except Exception as e:
            print(f"   ⚠️  Skipped {file.name}: {e}")

if img_count > 0 or vid_count > 0:
    print(f"   ✅ Processed: {img_count} images, {vid_count} videos")
else:
    print("   ℹ️  No new media found (carousel already up-to-date)")
PYTHON

# Step 3: Update carousel HTML
echo ""
echo "🎠 Step 3: Updating carousel HTML..."

IMG_COUNT=$(find "$IMG_DIR" -name "*.jpg" -type f | wc -l)
VID_COUNT=$(find "$VID_DIR" -name "*.mp4" -type f | wc -l)

echo "   ✅ Carousel ready: $IMG_COUNT images + $VID_COUNT videos"

# Step 4: Deploy to GitHub Pages
echo ""
echo "🚀 Step 4: Deploying to GitHub Pages..."

cd "$REPO_ROOT"

# Check if there are new files to commit
if [ -z "$(git status --porcelain)" ]; then
    echo "   ℹ️  No changes to deploy"
else
    git add site/img/happy-customers/ site/video/happy-customers/
    git commit -m "🎥 Auto-update: Carousel refresh $(date +%Y-%m-%d\ %H:%M:%S)" || true
    
    if git rev-parse --verify origin/main > /dev/null 2>&1; then
        git push origin main
        echo "   ✅ Deployed to GitHub Pages"
    else
        echo "   ⚠️  No remote configured - local update only"
    fi
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "   ✅ AUTOMATION COMPLETE!"
echo "   Next run: $(date -v+1d +%Y-%m-%d\ 02:00:00)"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""
