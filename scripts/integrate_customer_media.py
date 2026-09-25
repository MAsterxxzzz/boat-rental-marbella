#!/usr/bin/env python3
"""
Integrate new customer videos and photos into the Happy Customers carousel.
Place media files in the respective folders and run this script.
"""
import pathlib
import json
from PIL import Image
import subprocess
import os

# Website paths
SITE_ROOT = pathlib.Path(__file__).parent.parent / "site"
IMG_HC = SITE_ROOT / "img" / "happy-customers"
VID_HC = SITE_ROOT / "video" / "happy-customers"
INDEX_HTML = SITE_ROOT / "index.html"

# Create directories if they don't exist
IMG_HC.mkdir(parents=True, exist_ok=True)
VID_HC.mkdir(parents=True, exist_ok=True)

def optimize_image(src_path, dest_jpg, dest_webp):
    """Convert and optimize image to JPG and WebP"""
    try:
        img = Image.open(src_path)

        # Ensure RGB mode
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img

        # Save as JPG (width 220, height 391 per carousel)
        img.thumbnail((220, 391), Image.Resampling.LANCZOS)
        img.save(dest_jpg, 'JPEG', quality=85)
        img.save(dest_webp, 'WEBP', quality=85)

        return True
    except Exception as e:
        print(f"❌ Image optimization failed: {e}")
        return False

def create_video_poster(video_path, poster_path, timestamp="00:00:02"):
    """Extract first frame from video as poster image"""
    try:
        cmd = [
            'ffmpeg', '-i', str(video_path),
            '-ss', timestamp,
            '-vframes', '1',
            '-vf', 'scale=220:391:force_original_aspect_ratio=decrease',
            str(poster_path),
            '-y'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Poster creation failed: {e}")
        return False

def generate_carousel_html(media_items):
    """Generate HTML carousel items"""
    html_items = []

    for item in media_items:
        media_type = item['type']  # 'image' or 'video'
        filename = item['filename']
        caption = item.get('caption', 'Happy customers!')
        badge = item.get('badge', '')

        if media_type == 'image':
            name_base = filename.rsplit('.', 1)[0]
            html = f'''<div class="hc-card"><img src="/img/happy-customers/{name_base}.jpg" srcset="/img/happy-customers/{name_base}.webp 900w" alt="{caption}" loading="lazy" width="220" height="391"><div class="hc-caption">{caption}</div></div>'''
        else:  # video
            name_base = filename.rsplit('.', 1)[0]
            badge_html = f'<span class="hc-badge">{badge}</span>' if badge else ''
            html = f'''<div class="hc-card"><video autoplay muted loop playsinline preload="metadata" poster="/video/happy-customers/{name_base}.jpg" aria-label="{caption}"><source src="/video/happy-customers/{name_base}.mp4" type="video/mp4"></video>{badge_html}<div class="hc-caption">{caption}</div></div>'''

        html_items.append(html)

    return html_items

def list_pending_media():
    """Find unprocessed media files in temporary locations"""
    home = pathlib.Path.home()
    sources = [
        home / "Downloads" / "happy-customers",
        home / "Desktop" / "happy-customers",
        pathlib.Path("/tmp") / "happy-customers"
    ]

    media_files = {'images': [], 'videos': []}

    for source_dir in sources:
        if source_dir.exists():
            print(f"\n📂 Checking {source_dir}...")
            for f in sorted(source_dir.iterdir()):
                if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif'}:
                    media_files['images'].append(f)
                    print(f"  📷 {f.name}")
                elif f.suffix.lower() in {'.mp4', '.mov', '.avi', '.webm'}:
                    media_files['videos'].append(f)
                    print(f"  🎬 {f.name}")

    return media_files

def process_media_batch(media_dict):
    """Process a batch of media files"""
    print("\n🔄 Processing media files...\n")

    # Process images
    for img_path in media_dict['images']:
        name_base = img_path.stem
        dest_jpg = IMG_HC / f"{name_base}.jpg"
        dest_webp = IMG_HC / f"{name_base}.webp"

        print(f"📷 Processing {img_path.name}...")
        if optimize_image(img_path, dest_jpg, dest_webp):
            print(f"   ✅ Saved: {dest_jpg.name}, {dest_webp.name}")

    # Process videos
    for vid_path in media_dict['videos']:
        name_base = vid_path.stem
        dest_mp4 = VID_HC / f"{name_base}.mp4"
        dest_poster = VID_HC / f"{name_base}.jpg"

        print(f"🎬 Processing {vid_path.name}...")

        # Copy video (or re-encode if needed)
        if vid_path.suffix.lower() == '.mp4':
            import shutil
            shutil.copy2(vid_path, dest_mp4)
        else:
            # Re-encode to MP4
            cmd = ['ffmpeg', '-i', str(vid_path), '-c:v', 'libx264', '-preset', 'medium',
                   '-c:a', 'aac', str(dest_mp4), '-y']
            subprocess.run(cmd, capture_output=True)

        # Create poster
        if create_video_poster(vid_path if vid_path.suffix.lower() == '.mp4' else dest_mp4, dest_poster):
            print(f"   ✅ Saved: {dest_mp4.name}, {dest_poster.name}")

if __name__ == '__main__':
    print("🎬 Boat Rental Marbella — Customer Media Integration\n")
    print("=" * 60)

    # Check for media files
    print("\nStep 1: Looking for media files...")
    media = list_pending_media()

    if not media['images'] and not media['videos']:
        print("\n❌ No media files found. Please add image/video files to:")
        print(f"   • {pathlib.Path.home() / 'Downloads' / 'happy-customers'}")
        print(f"   • {pathlib.Path.home() / 'Desktop' / 'happy-customers'}")
        print("\nSupported formats:")
        print("   Images: .jpg, .png, .gif")
        print("   Videos: .mp4, .mov, .avi, .webm")
        exit(1)

    print(f"\n✅ Found {len(media['images'])} images, {len(media['videos'])} videos")

    # Process media
    process_media_batch(media)

    print("\n" + "=" * 60)
    print("✅ Media processing complete!")
    print(f"\nIntegrated media:")
    print(f"   Images: {IMG_HC}")
    print(f"   Videos: {VID_HC}")
    print(f"\nNext steps:")
    print("1. Review the media files in the above directories")
    print("2. Update /site/index.html with new carousel items")
    print("3. Deploy the website")
