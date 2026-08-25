#!/usr/bin/env python3
"""One-off helper: append gallery_local photo entries to a boat in
config/boats.json. Usage:

  python3 scripts/_add_gallery.py <slug> <name1>:<alt1> [<name2>:<alt2> ...]

Assumes site/img/boats/<slug>/<name>-{600,900,1200}.jpg already exist.
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOATS_PATH = ROOT / "config" / "boats.json"

def main():
    slug = sys.argv[1]
    entries = sys.argv[2:]
    data = json.loads(BOATS_PATH.read_text())
    boat = next((b for b in data["boats"] if b["slug"] == slug), None)
    if boat is None:
        print(f"ERROR: no boat with slug {slug}")
        sys.exit(1)
    boat.setdefault("gallery_local", [])
    for entry in entries:
        name, alt = entry.split(":", 1)
        boat["gallery_local"].append({
            "src": f"/img/boats/{slug}/{name}-1200.jpg",
            "srcset": [
                [f"/img/boats/{slug}/{name}-600.jpg", 600],
                [f"/img/boats/{slug}/{name}-900.jpg", 900],
                [f"/img/boats/{slug}/{name}-1200.jpg", 1200],
            ],
            "alt": alt,
        })
    BOATS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"{slug}: gallery now {len(boat['gallery_local'])} photos")

if __name__ == "__main__":
    main()
