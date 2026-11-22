"""
Master Profile Updater Script.
Orchestrates:
1. Fetching live contributions (or using cached data).
2. Generating animated heatmap SVG.
3. Generating improved Neofetch info card SVG.
4. Validating all generated SVGs.
"""

import os
import sys
import xml.etree.ElementTree as ET

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, PROJECT_ROOT)

from scripts.fetch_contributions import fetch_and_save
from scripts.generate_heatmap import generate_heatmap_svg
from scripts.generate_infocard import generate_infocard_svg


def validate_svg(path: str) -> bool:
    if not os.path.exists(path):
        print(f"Error: {path} does not exist", file=sys.stderr)
        return False
    size = os.path.getsize(path)
    if size < 200:
        print(f"Error: {path} is too small ({size} bytes)", file=sys.stderr)
        return False
    try:
        root = ET.parse(path).getroot()
        if not root.tag.endswith("svg"):
            print(f"Error: root tag is not svg ({root.tag})", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"Error parsing {path}: {e}", file=sys.stderr)
        return False


def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "charangowdamd-cmd"
    print(f"=== GitHub Profile Assets Update for @{username} ===")

    contributions_json = os.path.join(PROJECT_ROOT, "assets", "data", "contributions.json")
    heatmap_svg = os.path.join(PROJECT_ROOT, "assets", "heatmap.svg")
    infocard_svg = os.path.join(PROJECT_ROOT, "assets", "info-card.svg")

    # 1. Fetch contributions
    print("\n[1/3] Fetching contributions data...")
    try:
        fetch_and_save(username, contributions_json)
    except Exception as e:
        print(f"Fetch error: {e}", file=sys.stderr)
        if not os.path.exists(contributions_json):
            print("Fatal: no cached contributions.json found.", file=sys.stderr)
            sys.exit(1)
        print("Continuing with existing cached data.")

    # 2. Generate heatmap
    print("\n[2/3] Generating contribution heatmap SVG...")
    generate_heatmap_svg(contributions_json, heatmap_svg)

    # 3. Generate info card
    print("\n[3/3] Generating Neofetch info card SVG...")
    generate_infocard_svg(infocard_svg)

    # Validation
    print("\n=== Validation ===")
    all_ok = True
    for asset in [heatmap_svg, infocard_svg]:
        ok = validate_svg(asset)
        label = "PASSED" if ok else "FAILED"
        print(f"  {os.path.basename(asset)}: {label} ({os.path.getsize(asset):,} bytes)")
        all_ok = all_ok and ok

    if not all_ok:
        print("Fatal: asset validation failed.", file=sys.stderr)
        sys.exit(1)

    print("\nAll assets generated and validated successfully!")


if __name__ == "__main__":
    main()
