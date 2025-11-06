"""
Script to seed the database with sample satellites.

This script reads sample_satellites.json and creates satellites in the
database via the FastAPI endpoints.

Usage:
    python seed_database.py
"""

import json
import requests
from pathlib import Path

API_BASE_URL = "http://localhost:8000"


def seed_satellites():
    """Load sample satellites and add them to the database."""

    # Read sample data
    sample_file = Path(__file__).parent / "sample_satellites.json"

    with open(sample_file, "r") as f:
        satellites = json.load(f)

    print(f"Loading {len(satellites)} sample satellites...")
    print()

    for sat in satellites:
        try:
            response = requests.post(f"{API_BASE_URL}/satellites/", json=sat)
            response.raise_for_status()
            result = response.json()
            print(f"✓ Created: {sat['name']} (ID: {result['id']})")
        except requests.exceptions.HTTPException as e:
            if e.response.status_code == 400:
                print(f"⚠ Skipped: {sat['name']} (already exists)")
            else:
                print(f"✗ Failed: {sat['name']} - {e}")
        except Exception as e:
            print(f"✗ Failed: {sat['name']} - {e}")

    print()
    print("Done! View satellites at http://localhost:8000/satellites/")


if __name__ == "__main__":
    seed_satellites()
