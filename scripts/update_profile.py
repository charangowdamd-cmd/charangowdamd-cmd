"""
Master Profile Updater Script.
Orchestrates:
1. Fetching live contributions (or using cached data).
2. Generating animated heatmap SVG.
3. Compiling animated ASCII portrait SVG.
4. Generating Neofetch info card SVG.
5. Validating all generated SVGs.
"""

import os
import sys
import xml.etree.ElementTree as ET

# Add current directory to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, PROJECT_ROOT)

from scripts.fetch_contributions import fetch_and_save
from scripts.generate_heatmap import generate_heatmap_svg
from scripts.generate_ascii import build_ascii
from scripts.generate_infocard import generate_infocard_svg

def validate_svg(path: str) -> bool:
    if not os.path.exists(path):
        print(f"Error: {path} does not exist", file=sys.stderr)
        return False
    size = os.path.getsize(path)
    if size < 200:
        print(f"Error: {path} is suspiciously small ({size} bytes)", file=sys.stderr)
        return False
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        if not root.tag.endswith("svg"):
            print(f"Error: {path} root tag is not svg ({root.tag})", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"Error parsing XML in {path}: {e}", file=sys.stderr)
        return False

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "charangowdamd-cmd"
    print(f"=== Starting GitHub Profile Assets Update for @{username} ===")
    
    # Paths relative to project root
    contributions_json = os.path.join(PROJECT_ROOT, "assets", "data", "contributions.json")
    heatmap_svg = os.path.join(PROJECT_ROOT, "assets", "heatmap.svg")
    ascii_svg = os.path.join(PROJECT_ROOT, "assets", "ascii-portrait.svg")
    infocard_svg = os.path.join(PROJECT_ROOT, "assets", "info-card.svg")
    
    # 1. Fetch contributions
    print("\n[1/4] Fetching contributions data...")
    try:
        fetch_and_save(username, contributions_json)
    except Exception as e:
        print(f"Contribution fetch error: {e}", file=sys.stderr)
        if not os.path.exists(contributions_json):
            print("Fatal: No cached contributions.json available.", file=sys.stderr)
            sys.exit(1)
        print("Continuing with existing cached contributions.json.")

    # 2. Generate Heatmap SVG
    print("\n[2/4] Generating contribution heatmap SVG...")
    generate_heatmap_svg(contributions_json, heatmap_svg)

    # 3. Generate ASCII Portrait SVG
    print("\n[3/4] Generating ASCII portrait SVG...")
    photo_candidate = os.path.join(PROJECT_ROOT, "raw_photo.jpg")
    photo_arg = photo_candidate if os.path.exists(photo_candidate) else ""
    build_ascii(photo_arg)

    # 4. Generate Neofetch Info Card SVG
    print("\n[4/4] Generating Neofetch info card SVG...")
    generate_infocard_svg(infocard_svg)

    # Validation
    print("\n=== Validating Generated Assets ===")
    all_ok = True
    for asset in [heatmap_svg, ascii_svg, infocard_svg]:
        ok = validate_svg(asset)
        status = "PASSED" if ok else "FAILED"
        print(f"  {os.path.basename(asset)}: {status} ({os.path.getsize(asset):,} bytes)")
        if not ok:
            all_ok = False

    if not all_ok:
        print("Fatal: Asset validation failed.", file=sys.stderr)
        sys.exit(1)

    print("\nAll assets generated and validated successfully!")

if __name__ == "__main__":
    main()
