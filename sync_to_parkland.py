"""Sync static assets from bracket/docs/ to parkland Flask app.

Source of truth: E:/projects/bracket/docs/
Target:          E:/projects/parkland/parklandapp/

Usage:
    uv run sync_to_parkland.py          # copy all
    uv run sync_to_parkland.py --dry    # show what would be copied
"""

import argparse
import os
import shutil

SRC = os.path.join(os.path.dirname(__file__), "docs")
PARKLAND = os.path.join(os.path.dirname(__file__), "..", "parkland", "parklandapp")

STATIC_DST = os.path.join(PARKLAND, "static", "worldcup")
TEMPLATE_DST = os.path.join(PARKLAND, "templates", "worldcup")

# Directories to copy as static assets
STATIC_DIRS = ["css", "js", "data"]

# HTML files to copy as templates
HTML_GLOB = ".html"


def sync(dry_run=False):
    copied = 0

    # Static dirs (css/, js/, data/)
    for dirname in STATIC_DIRS:
        src_dir = os.path.join(SRC, dirname)
        dst_dir = os.path.join(STATIC_DST, dirname)

        if not os.path.isdir(src_dir):
            continue

        for root, _, files in os.walk(src_dir):
            for fname in files:
                src_file = os.path.join(root, fname)
                rel = os.path.relpath(src_file, SRC)
                dst_file = os.path.join(STATIC_DST, rel)

                if should_copy(src_file, dst_file):
                    if dry_run:
                        print(f"  [DRY] {rel} -> static/worldcup/{rel}")
                    else:
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                        print(f"  {rel} -> static/worldcup/{rel}")
                    copied += 1

    # HTML files -> templates
    for fname in os.listdir(SRC):
        if not fname.endswith(HTML_GLOB):
            continue

        src_file = os.path.join(SRC, fname)
        dst_file = os.path.join(TEMPLATE_DST, fname)

        if should_copy(src_file, dst_file):
            if dry_run:
                print(f"  [DRY] {fname} -> templates/worldcup/{fname}")
            else:
                os.makedirs(TEMPLATE_DST, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                print(f"  {fname} -> templates/worldcup/{fname}")
            copied += 1

    if copied == 0:
        print("  Everything up to date.")
    else:
        verb = "would copy" if dry_run else "copied"
        print(f"\n  {verb} {copied} file(s)")


def should_copy(src, dst):
    """Return True if dst doesn't exist or src is newer."""
    if not os.path.exists(dst):
        return True
    return os.path.getmtime(src) > os.path.getmtime(dst)


def main():
    parser = argparse.ArgumentParser(description="Sync bracket assets to parkland")
    parser.add_argument("--dry", action="store_true", help="Dry run — show what would be copied")
    args = parser.parse_args()

    print(f"Source:  {SRC}")
    print(f"Static:  {STATIC_DST}")
    print(f"Templates: {TEMPLATE_DST}")
    print()

    sync(dry_run=args.dry)


if __name__ == "__main__":
    main()
