# Happy Customers Media Requirements

**Status:** HTML Updated ✅ | Media Files Pending ⏳  
**Date:** September 25, 2026  
**Purpose:** New carousel items added to homepage - awaiting customer media files

---

## New Carousel Items Added

6 new carousel items have been added to the Happy Customers section. These are now active in the HTML and will display automatically once the corresponding media files are added to the website directories.

### Item 1: Friends Laughing (Video)
- **File name:** `group-laughing.mp4`
- **Poster image:** `group-laughing.jpg`
- **Caption:** "Friends laughing 😂"
- **Type:** Video  
- **Location:** `/site/video/happy-customers/group-laughing.mp4` and `group-laughing.jpg`
- **Source:** Google Drive Happy Customers folder

### Item 2: Golden Sunset (Image)
- **File name:** `sunset-moment.jpg`
- **WebP version:** `sunset-moment.webp`
- **Caption:** "Golden sunset 🌅"
- **Type:** Image  
- **Location:** `/site/img/happy-customers/sunset-moment.jpg` and `.webp`
- **Source:** Google Drive Happy Customers folder

### Item 3: Group Cheers (Video)
- **File name:** `group-cheers.mp4`
- **Poster image:** `group-cheers.jpg`
- **Caption:** "Cheers to good times 🥂"
- **Type:** Video  
- **Location:** `/site/video/happy-customers/group-cheers.mp4` and `group-cheers.jpg`
- **Source:** Google Drive Happy Customers folder

### Item 4: Scenic Coast (Image)
- **File name:** `scenic-coast.jpg`
- **WebP version:** `scenic-coast.webp`
- **Caption:** "Marbella coast beauty 📸"
- **Type:** Image  
- **Location:** `/site/img/happy-customers/scenic-coast.jpg` and `.webp`
- **Source:** Google Drive Happy Customers folder

### Item 5: Water Adventures (Video)
- **File name:** `adventure-moment.mp4`
- **Poster image:** `adventure-moment.jpg`
- **Caption:** "Water adventures 🌊"
- **Type:** Video  
- **Location:** `/site/video/happy-customers/adventure-moment.mp4` and `adventure-moment.jpg`
- **Source:** Google Drive Happy Customers folder

### Item 6: (Bonus placeholder if needed)
Can add one more item if desired from the Google Drive uploads.

---

## How to Add the Media Files

### Step 1: Locate files in Google Drive
Go to: https://drive.google.com/drive/folders/1qEQPlq6084s7eaq2wqTtoTjN5t2yvFlS

The uploaded files from Sept 25 include:
- Videos: `b48a4c8960ce4d7ba08a040f4045fb62.mov`, `066fa8a8bcce4ae8ba26248a347d28aa.mov`, etc.
- Photos: `IMG_0323.PNG`, `IMG_0324.PNG`, `20610673-ba71-419a-8728-1eb2d9a4fd86.jpg`, etc.

### Step 2: Process and rename files
For each video/photo from Google Drive:
1. Download it
2. Optimize using the `scripts/integrate_customer_media.py` script
3. Rename to match one of the items above (e.g., rename a friends video to `group-laughing.mp4`)

OR rename manually and place in correct directories:
- Videos go to: `/site/video/happy-customers/`
- Images go to: `/site/img/happy-customers/`

### Step 3: Create image variants
For images, you need both formats:
- `sunset-moment.jpg` (original JPEG, optimized)
- `sunset-moment.webp` (WebP version for modern browsers)

Use the integration script or online tools:
- https://tinyjpg.com (JPG compression)
- https://convertio.co (WebP conversion)

### Step 4: Create video posters
For videos, you need a poster frame:
- `group-cheers.mp4` (the video file)
- `group-cheers.jpg` (extracted first frame or meaningful scene)

Extract poster with FFmpeg:
```bash
ffmpeg -i group-cheers.mp4 -ss 00:00:02 -vframes 1 group-cheers.jpg
```

### Step 5: Verify files are in place
```bash
ls /Users/nunnu/Desktop/boathire/boat-rental-marbella/site/img/happy-customers/
ls /Users/nunnu/Desktop/boathire/boat-rental-marbella/site/video/happy-customers/
```

### Step 6: Deploy
```bash
cd /Users/nunnu/Desktop/boathire/boat-rental-marbella
git add site/img/happy-customers site/video/happy-customers site/index.html
git commit -m "Add new customer testimonial videos and photos to Happy Customers carousel"
git push origin main
```

---

## File Specifications

### Image Requirements
- **Format:** JPG (original) + WebP (optimized)
- **Dimensions:** Portrait 220×391px (carousel size), source should be larger (1440×2560px or more)
- **Quality:** High resolution, good lighting
- **File size:** 50-150 KB per image after optimization
- **Aspect ratio:** Vertical portrait (9:16)

### Video Requirements
- **Format:** MP4 (H.264 codec)
- **Duration:** 3-15 seconds (loops infinitely)
- **Bitrate:** 2-4 Mbps
- **Resolution:** 1080p minimum
- **Poster frame:** Extract at 2 seconds, save as JPG
- **File size:** 1-5 MB per video

---

## Mapping: Google Drive Files → Website Items

Map your downloaded Google Drive files to the 6 new carousel items:

| Item | Google Drive File | Website Filename | Type |
|------|------------------|------------------|------|
| Friends laughing | (group video from Sept 25) | group-laughing.mp4 | Video |
| Golden sunset | (sunset/coast photo) | sunset-moment.jpg | Image |
| Cheers moment | (celebration video) | group-cheers.mp4 | Video |
| Scenic coast | (beautiful coast photo) | scenic-coast.jpg | Image |
| Water adventure | (action/activity video) | adventure-moment.mp4 | Video |
| (Optional) | (additional photo/video) | (your choice) | Video/Image |

---

## Testing Before Deploy

Once files are in place, test locally:

```bash
# Start local server
cd /Users/nunnu/Desktop/boathire/boat-rental-marbella/site
python3 -m http.server 8000

# Visit: http://localhost:8000
# Scroll to "Happy customers on the water"
# Verify carousel shows new items
# Check that videos play and images load
```

---

## Current Carousel Stats

- **Total items:** 14 original + 6 new = 20 items
- **Images:** 10 items
- **Videos:** 10 items
- **Display style:** Infinite horizontal scroll
- **Loop behavior:** Seamless repeat (due to duplicate section)

---

## After Deploying

Once files are in place and deployed:

1. ✅ Website will automatically display new items in the carousel
2. ✅ Carousel will loop smoothly with 20+ items
3. ✅ Mobile users will see the same carousel
4. ✅ Video autoplay (muted) works on modern browsers
5. ✅ Social proof increases with real customer moments

---

## Questions?

Refer to: `CUSTOMER_MEDIA_INTEGRATION_GUIDE.md` for detailed steps  
Or: `MEDIA_INTEGRATION_QUICK_START.txt` for quick commands

---

**HTML Status:** ✅ Complete - carousel items in place  
**Media Status:** ⏳ Awaiting files from Google Drive  
**Deployment Status:** 🔲 Ready when files are added
