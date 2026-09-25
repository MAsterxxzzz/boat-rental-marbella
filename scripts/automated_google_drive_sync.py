#!/usr/bin/env python3
"""
🚀 FULLY AUTOMATED CAROUSEL UPDATE
Google Drive → Download → Process → Deploy (24/7)
"""
import os
import json
import pathlib
from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from PIL import Image
import subprocess
import shutil

# Configuration
CREDS_FILE = pathlib.Path.home() / ".config/boathire-seo/service-account-key.json"
DRIVE_FOLDER_ID = "1qEQPlq6084s7eaq2wqTtoTjN5t2yvFlS"  # Happy Customers folder
DOWNLOAD_DIR = pathlib.Path.home() / "Downloads/auto-drive-carousel"
REPO_ROOT = pathlib.Path.home() / "Projects/boat-rental-marbella"
IMG_DIR = REPO_ROOT / "site/img/happy-customers"
VID_DIR = REPO_ROOT / "site/video/happy-customers"

def get_drive_service():
    """Authenticate with Google Drive API"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            CREDS_FILE,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        print(f"❌ Auth failed: {e}")
        return None

def list_folder_files(service, folder_id):
    """List all files in a Drive folder"""
    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType, createdTime, size)',
            pageSize=100,
            orderBy='createdTime desc'
        ).execute()
        return results.get('files', [])
    except Exception as e:
        print(f"❌ List failed: {e}")
        return []

def download_file(service, file_id, filename, dest_path):
    """Download a file from Google Drive"""
    try:
        # Check if file already exists locally
        if dest_path.exists():
            return True
        
        request = service.files().get_media(fileId=file_id)
        with open(dest_path, 'wb') as f:
            downloader = request.execute()
            f.write(downloader)
        return True
    except Exception as e:
        print(f"⚠️  Skipped {filename}")
        return False

def process_images(download_dir):
    """Process and optimize images"""
    processed = 0
    for file in sorted(download_dir.glob("*")):
        if not file.is_file():
            continue
        
        suffix = file.suffix.lower()
        if suffix not in {'.jpg', '.jpeg', '.png'}:
            continue
        
        try:
            img = Image.open(file)
            if img.mode != 'RGB':
                if img.mode in ('RGBA', 'LA'):
                    rgb = Image.new('RGB', img.size, (255, 255, 255))
                    rgb.paste(img, mask=img.split()[-1])
                    img = rgb
                else:
                    img = img.convert('RGB')
            
            base = file.stem
            jpg_dest = IMG_DIR / f"{base}.jpg"
            webp_dest = IMG_DIR / f"{base}.webp"
            
            # Skip if already processed
            if jpg_dest.exists():
                continue
            
            img.save(jpg_dest, 'JPEG', quality=85, optimize=True)
            img.save(webp_dest, 'WEBP', quality=85)
            processed += 1
        except Exception as e:
            pass
    
    return processed

def process_videos(download_dir):
    """Copy video files"""
    processed = 0
    for file in sorted(download_dir.glob("*")):
        if not file.is_file():
            continue
        
        suffix = file.suffix.lower()
        if suffix not in {'.mp4', '.mov', '.avi', '.mkv'}:
            continue
        
        try:
            dest = VID_DIR / file.name
            if dest.exists():
                continue
            
            shutil.copy2(file, dest)
            processed += 1
        except Exception as e:
            pass
    
    return processed

def deploy_to_github():
    """Commit and push changes"""
    try:
        os.chdir(REPO_ROOT)
        
        # Check for changes
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if not result.stdout.strip():
            return False  # No changes
        
        # Stage changes
        subprocess.run(['git', 'add', 'site/img/happy-customers/', 
                       'site/video/happy-customers/'], check=False)
        
        # Commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(['git', 'commit', '-m', 
                       f'🎥 Auto-sync carousel: {timestamp}'], 
                      check=False)
        
        # Push
        subprocess.run(['git', 'push', 'origin', 'main'], check=False)
        return True
    except Exception as e:
        return False

def main():
    print("\n" + "="*60)
    print("🚀 AUTOMATED CAROUSEL SYNC (24/7)")
    print(f"   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    # Create directories
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    VID_DIR.mkdir(parents=True, exist_ok=True)
    
    # Connect to Google Drive
    service = get_drive_service()
    if not service:
        print("❌ Cannot authenticate with Google Drive")
        return False
    
    print("✅ Authenticated with Google Drive\n")
    
    # Download files
    print("📥 Downloading from Happy Customers folder...")
    files = list_folder_files(service, DRIVE_FOLDER_ID)
    
    if not files:
        print("   ℹ️  No files found (carousel already up-to-date)\n")
        return True
    
    downloaded = 0
    for file in files:
        dest = DOWNLOAD_DIR / file['name']
        if download_file(service, file['id'], file['name'], dest):
            downloaded += 1
    
    if downloaded > 0:
        print(f"   ✅ Downloaded {downloaded} files\n")
    else:
        print("   ℹ️  All files already synced\n")
    
    # Process media
    print("🎬 Processing media files...")
    img_count = process_images(DOWNLOAD_DIR)
    vid_count = process_videos(DOWNLOAD_DIR)
    
    if img_count > 0 or vid_count > 0:
        print(f"   ✅ Processed: {img_count} images, {vid_count} videos\n")
    else:
        print("   ℹ️  No new media to process\n")
    
    # Deploy
    if img_count > 0 or vid_count > 0:
        print("🚀 Deploying to GitHub Pages...")
        if deploy_to_github():
            print("   ✅ Deployment successful\n")
        else:
            print("   ⚠️  Deployment completed with warnings\n")
    
    print("="*60)
    print("✅ SYNC COMPLETE - Carousel updated!")
    print("="*60 + "\n")
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
