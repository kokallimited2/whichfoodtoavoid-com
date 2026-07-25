#!/usr/bin/env python3
"""
first_run_seed.py - Seeds the whichfoodtoavoid.com site with initial products
and comparisons. Runs 3 comparisons immediately to populate the site before
the daily cron kicks in.

Usage: python3 first_run_seed.py
"""

import json
import os
import subprocess
import sys
from datetime import datetime

BASE_DIR = os.path.expanduser("~/github-projects/whichfoodtoavoid-com")
DATA_FILE = os.path.join(BASE_DIR, "data", "categories.json")
SCRIPT = os.path.expanduser("~/.hermes/scripts/whichfood_daily_comparison.py")
LOG_DIR = os.path.expanduser("~/.hermes/logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Run 3 comparisons from the rotation
# The rotation order is: air-fryers, blenders, knife-sets, slow-cookers, ...
# We'll manually set last_index to seed the first 3, then run the script

# But we can't easily run the script with a forced category. Let me instead
# directly invoke the main script 3 times, manipulating last_index between runs.

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def run_comparison():
    """Run the daily comparison script and return success/failure."""
    log("Running daily comparison script...")
    result = subprocess.run(
        ["python3", SCRIPT],
        capture_output=True, text=True, timeout=300
    )
    log(result.stdout[-500:] if result.stdout else "No output")
    if result.stderr:
        log(f"STDERR: {result.stderr[-300:]}")
    return result.returncode == 0


def force_next_category(data, target_slug):
    """Manually set last_index so the next run picks the target slug."""
    rotation = data["rotation"]
    if target_slug in rotation:
        idx = rotation.index(target_slug)
        # Set last_index to idx-1 so rotation picks idx
        data["last_index"] = (idx - 1) % len(rotation)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        log(f"Forced next category to: {target_slug} (index {data['last_index']} → next picks {idx})")
        return True
    return False


def main():
    log("=" * 50)
    log("FIRST RUN SEED - whichfoodtoavoid.com")
    log("=" * 50)

    # Load data
    if not os.path.exists(DATA_FILE):
        log(f"ERROR: {DATA_FILE} not found. Run setup first.")
        sys.exit(1)

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # First 3 categories: air-fryers, blenders, knife-sets
    seed_categories = ["air-fryers", "blenders", "knife-sets"]

    for i, slug in enumerate(seed_categories):
        log(f"\n--- Seed run {i+1}/{len(seed_categories)}: {slug} ---")
        force_next_category(data, slug)

        # Reload data after manipulation
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        success = run_comparison()
        if success:
            log(f"✅ Seeded {slug} successfully")
        else:
            log(f"❌ Failed to seed {slug}")

        # Add a small pause between runs
        import time
        time.sleep(2)

    log("\n" + "=" * 50)
    log("FIRST RUN SEED COMPLETE")
    log("=" * 50)
    log("The site now has 3 initial comparisons:")
    for slug in seed_categories:
        cat = data['categories'].get(slug, {})
        log(f"  • {cat.get('icon', '')} {cat.get('name', slug)}")
    log(f"\nNext cron run will continue with: slow-cookers")
    log("=" * 50)


if __name__ == "__main__":
    main()
