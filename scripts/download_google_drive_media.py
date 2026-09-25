#!/usr/bin/env python3
"""
Download latest media from Google Drive Happy Customers folder
Uses gdown to download shared Google Drive files
"""

import subprocess
import pathlib
import shutil

# Google Drive folder ID for Happy Customers
FOLDER_ID = "1qEQPlq6084s7eaq2wqTtoTjN5t2yvFlS"
FOLDER_URL = f"https://drive.google.com/drive/folders/{FOLDER_ID}"

# Destination
DOWNLOAD_DIR = pathlib.Path.home() / "Downloads" / "happy-customers-today"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "="*70)
print("🔽 DOWNLOADING FROM GOOGLE DRIVE - HAPPY CUSTOMERS FOLDER")
print("="*70 + "\n")

print(f"📁 Folder: {FOLDER_URL}")
print(f"📥 Downloading to: {DOWNLOAD_DIR}\n")

# Try to use gdown to download entire folder
try:
    cmd = ["gdown", "--folder", FOLDER_URL, "-O", str(DOWNLOAD_DIR), "--quiet"]
    print("Attempting to download folder with gdown...\n")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode == 0:
        print("✅ Download complete!\n")
    else:
        print(f"⚠️ gdown output: {result.stderr[:200]}\n")

except FileNotFoundError:
    print("⚠️ gdown not found. Installing...\n")
    subprocess.run(["pip3", "install", "gdown", "-q"], check=True)

    cmd = ["gdown", "--folder", FOLDER_URL, "-O", str(DOWNLOAD_DIR), "--quiet"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode == 0:
        print("✅ Download complete!\n")
except Exception as e:
    print(f"⚠️ Error: {e}\n")

# List what was downloaded
print("📂 Downloaded files:")
if DOWNLOAD_DIR.exists():
    files = list(DOWNLOAD_DIR.rglob("*"))
    files = [f for f in files if f.is_file()]

    for f in sorted(files):
        size = f.stat().st_size
        if size > 1024*1024:
            print(f"   ✅ {f.name} ({size/(1024*1024):.1f} MB)")
        else:
            print(f"   ✅ {f.name} ({size/1024:.0f} KB)")

    print(f"\n✅ Total: {len(files)} files downloaded")
else:
    print("   ❌ Download folder not found")

print("\n" + "="*70)
print("✅ FILES READY FOR INTEGRATION")
print("="*70 + "\n")
