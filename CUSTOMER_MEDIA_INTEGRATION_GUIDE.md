# Customer Media Integration Guide

**Last Updated:** September 25, 2026  
**Task:** Integrate new Happy Customers videos and photos into the website carousel

---

## Overview

The Happy Customers carousel on the website homepage displays customer experiences from boat charters. You've uploaded new videos and photos to the Google Drive "Happy Customers" folder. This guide explains how to process and integrate them into the website.

### Files Ready for Integration

**From Google Drive (Happy Customers folder):**

**Recent Videos (today's uploads):**
- `b48a4c8960ce4d7ba08a040f4045fb62.mov` (8.1 MB)
- `066fa8a8bcce4ae8ba26248a347d28aa.mov` (10.3 MB)
- `304f4ef6958b4bc7bec490d40f9a1e45.mov` (3.5 MB)
- `b7060e392835456eb2634bb75e496f83.mov` (3.6 MB)
- `12e22534-2b94-4987-91a5-e9d28ec93c94.mp4` (898 kB)
- `931994e0-5b91-44d5-ad1e-4d1af924af9b.mp4` (1.8 MB)
- `ScreenRecording_09-25-2026 08-18-16_1.mp4` (24.2 MB)

**Recent Photos:**
- `20610673-ba71-419a-8728-1eb2d9a4fd86.jpg` (218 kB)
- `f98cdcd5-8b66-4f56-9e54-5e388d67ac5f.jpg` (148 kB)
- `546a436d-2ae9-4d24-a730-16ab890f54c8.jpg` (112 kB)
- `IMG_0323.PNG` (447 kB)
- `IMG_0324.PNG` (466 kB)

---

## Step-by-Step Integration

### Step 1: Download Files from Google Drive

1. Go to: https://drive.google.com/drive/folders/1qEQPlq6084s7eaq2wqTtoTjN5t2yvFlS
2. Select the video and photo files you want to add
3. Click **Download** to save them locally
4. Extract the ZIP file to one of these locations:
   - `~/Downloads/happy-customers/`
   - `~/Desktop/happy-customers/`

### Step 2: Prepare Your Environment

Ensure you have the required tools installed:

```bash
# Check for Python 3.9+
python3 --version

# Check for FFmpeg (needed for video processing)
ffmpeg -version

# Check for PIL/Pillow
pip3 install pillow
```

### Step 3: Run the Integration Script

The `scripts/integrate_customer_media.py` script automates:
- Image optimization (JPG + WebP versions)
- Video poster frame extraction
- File organization into the correct directories

```bash
cd /Users/nunnu/Desktop/boathire/boat-rental-marbella
python3 scripts/integrate_customer_media.py
```

**Expected output:**
```
🎬 Boat Rental Marbella — Customer Media Integration

========================================================

Step 1: Looking for media files...

📂 Checking /Users/nunnu/Downloads/happy-customers...
  📷 group-laughing.jpg
  🎬 boat-sunset.mp4
  
✅ Found 5 images, 3 videos

🔄 Processing media files...

📷 Processing group-laughing.jpg...
   ✅ Saved: group-laughing.jpg, group-laughing.webp

🎬 Processing boat-sunset.mp4...
   ✅ Saved: boat-sunset.mp4, boat-sunset.jpg

... [more files]

========================================================
✅ Media processing complete!
```

### Step 4: Update the HTML Carousel

Once processed, add the new items to `/site/index.html` in the happy-customers section.

**Location in HTML:** Line 164-165 (inside the `<div class="hc-track">`)

#### Adding Image Cards

```html
<div class="hc-card">
  <img src="/img/happy-customers/group-laughing.jpg" 
       srcset="/img/happy-customers/group-laughing.webp 900w" 
       alt="Friends laughing on the boat 😂" 
       loading="lazy" width="220" height="391">
  <div class="hc-caption">Friends laughing on the boat 😂</div>
</div>
```

#### Adding Video Cards

```html
<div class="hc-card">
  <video autoplay muted loop playsinline preload="metadata" 
         poster="/video/happy-customers/boat-sunset.jpg" 
         aria-label="Golden hour on the water ✨">
    <source src="/video/happy-customers/boat-sunset.mp4" type="video/mp4">
  </video>
  <div class="hc-caption">Golden hour on the water ✨</div>
</div>
```

#### Adding Video Cards with Badge

For special moments (wildlife, celebrations, etc.):

```html
<div class="hc-card">
  <video autoplay muted loop playsinline preload="metadata" 
         poster="/video/happy-customers/dolphins.jpg" 
         aria-label="Dolphins visit us 🐬">
    <source src="/video/happy-customers/dolphins.mp4" type="video/mp4">
  </video>
  <span class="hc-badge">🐬 Wildlife</span>
  <div class="hc-caption">Dolphins visit us 🐬</div>
</div>
```

### Step 5: Test Locally

Before deploying, test the carousel:

```bash
# Navigate to the site directory
cd /Users/nunnu/Desktop/boathire/boat-rental-marbella/site

# Open in a local server (if you have Python)
python3 -m http.server 8000

# Visit http://localhost:8000 and check the carousel
```

### Step 6: Deploy to Production

Once tested:

```bash
cd /Users/nunnu/Desktop/boathire/boat-rental-marbella

# Commit the changes
git add site/img/happy-customers/ site/video/happy-customers/ site/index.html
git commit -m "Add new customer testimonial videos and photos to Happy Customers carousel"

# Push to GitHub
git push origin main

# The site will auto-deploy via GitHub Pages
```

---

## File Organization

After running the integration script, your files will be organized as:

```
site/
├── img/happy-customers/
│   ├── group-laughing.jpg      ← Original JPG
│   ├── group-laughing.webp     ← Optimized WebP
│   ├── sunset-cruise.jpg
│   ├── sunset-cruise.webp
│   └── ... (other images)
│
└── video/happy-customers/
    ├── boat-sunset.mp4         ← Video file
    ├── boat-sunset.jpg         ← Poster frame
    ├── dolphins.mp4
    ├── dolphins.jpg
    └── ... (other videos)
```

---

## Best Practices

### Image Guidelines

- **Aspect ratio:** Ideally 220px × 391px (portrait)
- **Formats:** JPG or PNG (the script converts to both JPG and WebP)
- **Quality:** High resolution (1440px × 2560px or larger)
- **Content:** Customer experiences, moments of joy, special occasions

### Video Guidelines

- **Duration:** 3-15 seconds (auto-looping)
- **Format:** MP4 (MOV files are converted automatically)
- **Bitrate:** 2-4 Mbps for web (the script optimizes automatically)
- **Aspect ratio:** Landscape (16:9) or square (1:1)
- **Content:** Action moments, reactions, scenic backdrop

### Captions

Write engaging captions with emojis:
- ✅ "Friends laughing on the bow 😂"
- ✅ "Sunset golden hour 🌅"
- ✅ "Birthday squad celebrating 🎂"
- ❌ "photo1.jpg"
- ❌ "Customers"

### Badges

Use badges for special categories:
- 🐬 Wildlife
- 🎂 Celebration
- 🌅 Scenic
- 💍 Wedding
- 🎉 Event

---

## Troubleshooting

### "Module not found: PIL"
```bash
pip3 install pillow
```

### "ffmpeg not found"
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Script doesn't find my files
- Ensure files are in `~/Downloads/happy-customers/` or `~/Desktop/happy-customers/`
- Check file permissions: `chmod 644 filename`
- Try absolute path: `/Users/YOUR_USERNAME/Downloads/happy-customers/`

### HTML carousel not updating
- Clear browser cache: `Cmd+Shift+R` (Chrome/Firefox)
- Check that images/videos are in correct directories
- Verify file paths in HTML match actual filenames (case-sensitive)

### Video doesn't play
- Ensure MP4 codec is H.264
- Check poster image exists in video directory
- Verify video dimensions are reasonable (not 8K or extreme aspect ratio)

---

## Manual Alternative (if script doesn't work)

If the Python script encounters issues, you can manually:

1. **Optimize images** using online tools:
   - https://tinyjpg.com (JPG compression)
   - https://convertio.co (WebP conversion)

2. **Extract video posters** using FFmpeg directly:
   ```bash
   ffmpeg -i input.mp4 -ss 00:00:02 -vframes 1 output.jpg
   ```

3. **Copy files** to the correct directories:
   ```bash
   cp optimized.jpg ~/Desktop/boathire/boat-rental-marbella/site/img/happy-customers/
   cp optimized.webp ~/Desktop/boathire/boat-rental-marbella/site/img/happy-customers/
   cp video.mp4 ~/Desktop/boathire/boat-rental-marbella/site/video/happy-customers/
   cp poster.jpg ~/Desktop/boathire/boat-rental-marbella/site/video/happy-customers/
   ```

4. **Manually add HTML** items to `/site/index.html` (see Step 4 above)

---

## Success Checklist

- [ ] Downloaded media files from Google Drive
- [ ] Created `~/Downloads/happy-customers/` folder
- [ ] Moved media files to the folder
- [ ] Ran `python3 scripts/integrate_customer_media.py`
- [ ] Verified files in `site/img/happy-customers/` and `site/video/happy-customers/`
- [ ] Added new carousel items to `site/index.html`
- [ ] Tested locally at http://localhost:8000
- [ ] Committed changes: `git commit -m "..."`
- [ ] Pushed to main: `git push origin main`
- [ ] Website updated at https://boatrentalinmarbella.com

---

## Questions?

For issues with the integration process, check:
- Script output messages (they explain problems)
- File permissions (`ls -la` in the directories)
- Browser console for JavaScript errors (`F12`)
- Git status before pushing: `git status`

Happy customers = happy business! 🚤
