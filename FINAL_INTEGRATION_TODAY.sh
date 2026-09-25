#!/bin/bash

# FINAL: Integrate TODAY's customer media uploads from Google Drive
# Files uploaded to Happy Customers folder on Sept 25, 2026

echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║           FINAL INTEGRATION: TODAY'S HAPPY CUSTOMERS MEDIA             ║"
echo "║            Google Drive → Website (Sept 25, 2026 Uploads)              ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

SITE_IMG="$HOME/Projects/boat-rental-marbella/site/img/happy-customers"
SITE_VID="$HOME/Projects/boat-rental-marbella/site/video/happy-customers"
DOWNLOAD_DIR="$HOME/Downloads/happy-customers-today"

echo "📂 Files needed from Google Drive Happy Customers folder (Sept 25):"
echo ""
echo "   VIDEOS:"
echo "   ✓ b48a4c8960ce4d7ba08a040f4045fb62.mov (8.1 MB)"
echo "   ✓ 066fa8a8bcce4ae8ba26248a347d28aa.mov (10.3 MB)"
echo "   ✓ 304f4ef6958b4bc7bec490d40f9a1e45.mov (3.5 MB)"
echo "   ✓ b7060e392835456eb2634bb75e496f83.mov (3.6 MB)"
echo "   ✓ 12e22534-2b94-4987-91a5-e9d28ec93c94.mp4 (898 kB)"
echo "   ✓ 931994e0-5b91-44d5-ad1e-4d1af924af9b.mp4 (1.8 MB)"
echo "   ✓ ScreenRecording_09-25-2026 08-18-16_1.mp4 (24.2 MB)"
echo ""
echo "   PHOTOS:"
echo "   ✓ 20610673-ba71-419a-8728-1eb2d9a4fd86.jpg (218 kB)"
echo "   ✓ f98cdcd5-8b66-4f56-9e54-5e388d67ac5f.jpg (148 kB)"
echo "   ✓ 546a436d-2ae9-4d24-a730-16ab890f54c8.jpg (112 kB)"
echo "   ✓ IMG_0323.PNG (447 kB)"
echo "   ✓ IMG_0324.PNG (466 kB)"
echo ""

# Check if we can access files that were already attempted to be downloaded
if [ -d "$DOWNLOAD_DIR" ]; then
    echo "📥 Checking for downloaded files in $DOWNLOAD_DIR..."
    FILE_COUNT=$(find "$DOWNLOAD_DIR" -type f | wc -l)
    if [ "$FILE_COUNT" -gt 0 ]; then
        echo "   ✅ Found $FILE_COUNT files to process"
        echo ""

        # Run the integration script
        python3 << 'PYTHON_EOF'
import pathlib
import shutil
from PIL import Image

DOWNLOAD_DIR = pathlib.Path.home() / "Downloads" / "happy-customers-today"
SITE_IMG = pathlib.Path.home() / "Projects" / "boat-rental-marbella" / "site" / "img" / "happy-customers"
SITE_VID = pathlib.Path.home() / "Projects" / "boat-rental-marbella" / "site" / "video" / "happy-customers"

processed = 0

# Process all downloaded media
for file in sorted(DOWNLOAD_DIR.rglob("*")):
    if not file.is_file():
        continue

    suffix = file.suffix.lower()

    if suffix in {'.mp4', '.mov'}:
        # Copy video files
        new_name = file.name  # Keep original name for now
        dest = SITE_VID / new_name
        shutil.copy2(file, dest)
        print(f"   ✅ Video: {new_name}")
        processed += 1

    elif suffix in {'.jpg', '.jpeg', '.png'}:
        # Process images
        try:
            img = Image.open(file)
            if img.mode != 'RGB':
                if img.mode in ('RGBA', 'LA'):
                    rgb = Image.new('RGB', img.size, (255, 255, 255))
                    rgb.paste(img, mask=img.split()[-1])
                    img = rgb
                else:
                    img = img.convert('RGB')

            # Save as JPG and WebP
            base_name = file.stem
            jpg_path = SITE_IMG / f"{base_name}.jpg"
            webp_path = SITE_IMG / f"{base_name}.webp"

            img.save(jpg_path, 'JPEG', quality=85, optimize=True)
            img.save(webp_path, 'WEBP', quality=85)

            print(f"   ✅ Image: {base_name}.jpg + .webp")
            processed += 1
        except Exception as e:
            print(f"   ❌ Failed to process {file.name}: {e}")

print(f"\n✅ Processed {processed} media files")

PYTHON_EOF
    else
        echo "   ⏳ No files found yet in $DOWNLOAD_DIR"
        echo ""
        echo "📋 NEXT STEPS:"
        echo ""
        echo "   1. Open Google Drive Happy Customers folder:"
        echo "      https://drive.google.com/drive/folders/1qEQPlq6084s7eaq2wqTtoTjN5t2yvFlS"
        echo ""
        echo "   2. Select ALL files uploaded today (Sept 25, 2026)"
        echo ""
        echo "   3. Click Download → Extract to:"
        echo "      $DOWNLOAD_DIR"
        echo ""
        echo "   4. Once extracted, run this script again"
        echo ""
        exit 1
    fi
else
    echo "   ⏳ Download directory not found"
    echo ""
    echo "📋 TO ADD YOUR TODAY'S UPLOADS:"
    echo ""
    echo "   1. Create the folder:"
    mkdir -p "$DOWNLOAD_DIR"
    echo "      ✅ mkdir -p $DOWNLOAD_DIR"
    echo ""
    echo "   2. Go to: https://drive.google.com/drive/folders/1qEQPlq6084s7eaq2wqTtoTjN5t2yvFlS"
    echo ""
    echo "   3. Select all files from Sept 25 and download"
    echo ""
    echo "   4. Extract them into: $DOWNLOAD_DIR"
    echo ""
    echo "   5. Run this script again to integrate"
    echo ""
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "   When you add the downloaded files, your carousel will show:"
echo "   • All 7 new videos from today"
echo "   • All 5 new photos from today"
echo "   • Perfect social proof for customers!"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""
