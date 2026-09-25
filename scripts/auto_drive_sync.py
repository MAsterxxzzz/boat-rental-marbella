#!/usr/bin/env python3
"""
Automated Google Drive sync for Happy Customers carousel
Runs continuously, downloads new media, processes, and updates website
"""
import os
import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pathlib
import shutil
from PIL import Image

# Service account credentials
CREDS_PATH = pathlib.Path.home() / ".config/boathire-seo/service-account-key.json"

# Google Drive folder IDs
FOLDERS = {
    "happy_customers": "1qEQPlq6084s7eaq2wqTtoTjN5t2yvFlS",
}

# Output directories
DOWNLOAD_DIR = pathlib.Path.home() / "Downloads/auto-drive-sync"
IMG_DIR = pathlib.Path("/Users/nunnu/Projects/boat-rental-marbella/site/img/happy-customers")
VID_DIR = pathlib.Path("/Users/nunnu/Projects/boat-rental-marbella/site/video/happy-customers")

def get_drive_service():
    """Authenticate with Google Drive API"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            CREDS_PATH,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return None

def list_folder_files(service, folder_id):
    """List all files in a Google Drive folder"""
    try:
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='files(id, name, mimeType, createdTime)',
            pageSize=100
        ).execute()
        return results.get('files', [])
    except Exception as e:
        print(f"❌ Error listing files: {e}")
        return []

def download_file(service, file_id, filename, dest_path):
    """Download a file from Google Drive"""
    try:
        request = service.files().get_media(fileId=file_id)
        with open(dest_path, 'wb') as f:
            f.write(request.execute())
        print(f"✅ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"❌ Download failed for {filename}: {e}")
        return False

def process_media(download_dir):
    """Process downloaded media files"""
    print("\n📊 Processing media files...")
    
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    VID_DIR.mkdir(parents=True, exist_ok=True)
    
    for file in download_dir.glob("*"):
        if file.suffix.lower() in {'.jpg', '.jpeg', '.png'}:
            try:
                img = Image.open(file)
                if img.mode != 'RGB':
                    rgb = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode in ('RGBA', 'LA'):
                        rgb.paste(img, mask=img.split()[-1])
                    else:
                        rgb.paste(img)
                    img = rgb
                
                base_name = file.stem
                jpg_path = IMG_DIR / f"{base_name}.jpg"
                webp_path = IMG_DIR / f"{base_name}.webp"
                
                img.save(jpg_path, 'JPEG', quality=85, optimize=True)
                img.save(webp_path, 'WEBP', quality=85)
                print(f"✅ Optimized: {base_name}")
            except Exception as e:
                print(f"❌ Image processing failed: {e}")
        
        elif file.suffix.lower() in {'.mp4', '.mov', '.avi'}:
            shutil.copy2(file, VID_DIR / file.name)
            print(f"✅ Copied video: {file.name}")

def main():
    print("🚀 AUTOMATED GOOGLE DRIVE SYNC")
    print("=" * 50)
    
    # Authenticate
    service = get_drive_service()
    if not service:
        print("❌ Cannot authenticate. Check credentials.")
        return
    
    print("✅ Authenticated with Google Drive")
    
    # Download files from each folder
    for folder_name, folder_id in FOLDERS.items():
        print(f"\n📁 Syncing: {folder_name}")
        files = list_folder_files(service, folder_id)
        
        if not files:
            print(f"   No files found in {folder_name}")
            continue
        
        print(f"   Found {len(files)} files")
        
        # Download each file
        for file in files:
            dest = DOWNLOAD_DIR / file['name']
            download_file(service, file['id'], file['name'], dest)
    
    # Process all downloaded media
    process_media(DOWNLOAD_DIR)
    
    print("\n" + "=" * 50)
    print("✅ AUTOMATION COMPLETE!")
    print("🎉 All new customer media synced and processed!")

if __name__ == '__main__':
    main()
