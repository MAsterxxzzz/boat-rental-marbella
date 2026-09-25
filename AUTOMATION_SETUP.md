# 🚀 BOAT RENTAL MARBELLA - FULL AUTOMATED CAROUSEL UPDATE (24/7)

## ✅ AUTOMATION COMPLETE

All components are now configured for **fully automated carousel updates without manual intervention**.

---

## 📋 WHAT'S AUTOMATED

- **Google Drive Integration**: Monitors the "Happy Customers" folder continuously
- **File Downloads**: Automatically downloads new photos and videos from Drive
- **Media Processing**: Optimizes images (JPG + WebP) and processes videos
- **Website Update**: Updates carousel HTML with new customer media
- **GitHub Deployment**: Commits and pushes changes to GitHub Pages automatically
- **Scheduled Runs**: Executes every 6 hours (2 AM, 8 AM, 2 PM, 8 PM UTC+0)

---

## 🔑 AUTHENTICATION

**Service Account**: `boathire-seo-agent@boathire-seo.iam.gserviceaccount.com`
**Google Cloud Project**: boathire-seo (Project ID: boathire-seo)
**Credentials File**: `~/.config/boathire-seo/service-account-key.json`
**Drive API**: ✅ ENABLED
**Access Level**: Read-only access to Google Drive (secure by design)

---

## 📂 FILES & LOCATIONS

**Automation Script**: `/Users/nunnu/Projects/boat-rental-marbella/scripts/automated_google_drive_sync.py`

**Scheduler Config**: `/Users/nunnu/Library/LaunchAgents/com.boathire.carousel-automation.plist`

**Carousel Media Directories**:
- Images: `/Users/nunnu/Projects/boat-rental-marbella/site/img/happy-customers/`
- Videos: `/Users/nunnu/Projects/boat-rental-marbella/site/video/happy-customers/`

**Logs**:
- Success Log: `/tmp/carousel-automation.log`
- Error Log: `/tmp/carousel-automation-error.log`

---

## 🕐 SCHEDULE

Automation runs **4 times per day** (every 6 hours):

| Time (UTC) | Time (EET/UTC+3) |
|-----------|-----------------|
| 02:00 | 05:00 |
| 08:00 | 11:00 |
| 14:00 | 17:00 |
| 20:00 | 23:00 |

To check logs after a run:
```bash
tail -f /tmp/carousel-automation.log
```

---

## 🎯 HOW IT WORKS (FLOW)

```
Google Drive Happy Customers Folder
          ↓
    [Auto Download]
          ↓
   Optimize Media Files
   (JPG + WebP for images)
          ↓
    Update Carousel HTML
          ↓
    Git Commit & Push
          ↓
  GitHub Pages Deploy
          ↓
  ✨ LIVE ON WEBSITE
```

---

## ✨ WHAT YOU SEE

Every time new customer photos/videos are uploaded to the Drive's "Happy Customers" folder, they will:

1. **Within 6 hours**: Automatically appear in the carousel
2. **Optimized**: Processed for web (JPG + WebP, compressed videos)
3. **Live**: Visible on boatrentalinmarbella.com carousel section

No manual work needed. Ever. 🤖

---

## 🔐 SECURITY

- ✅ Service account has **read-only** access to Drive
- ✅ Credentials stored securely in home directory
- ✅ No passwords or personal credentials used
- ✅ API keys automatically managed by Google Cloud
- ✅ Separate service account for this automation

---

## 📞 TROUBLESHOOTING

**If carousel isn't updating**:
1. Check logs: `tail /tmp/carousel-automation.log`
2. Verify scheduler is active: `launchctl list | grep carousel`
3. Test manually: `python3 /Users/nunnu/Projects/boat-rental-marbella/scripts/automated_google_drive_sync.py`

**To manually trigger right now**:
```bash
python3 /Users/nunnu/Projects/boat-rental-marbella/scripts/automated_google_drive_sync.py
```

**To disable automation**:
```bash
launchctl unload /Users/nunnu/Library/LaunchAgents/com.boathire.carousel-automation.plist
```

**To re-enable automation**:
```bash
launchctl load /Users/nunnu/Library/LaunchAgents/com.boathire.carousel-automation.plist
```

---

## 🎉 STATUS

**FULLY AUTOMATED** ✅  
Upload to Drive → Auto-sync within 6 hours → Live on website

No intervention required. Carousel stays fresh with customer moments 24/7.

---

*Last Updated: 2026-09-25*
*Automation Status: ACTIVE*
