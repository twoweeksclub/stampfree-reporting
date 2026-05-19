"""
Trustpilot Multi-Company Scraper
Uses Apify actor memo23/trustpilot-scraper-ppe
Scrapes 1-3 star reviews for multiple companies over last 30 days, saves as JSON.

Usage:
    pip install requests
    python trustpilot_scraper.py
"""

import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# CONFIG — edit these
# ─────────────────────────────────────────────

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
ACTOR_ID = "memo23~trustpilot-scraper-ppe"
MAX_TOTAL_CHARGE_USD = 6.30  # ~£5

COMPANIES = [
    "https://www.trustpilot.com/review/therugshopuk.co.uk",
    "https://www.trustpilot.com/review/rugsdirect.co.uk",
    "https://www.trustpilot.com/review/therugswarehouse.co.uk",
    "https://www.trustpilot.com/review/ruglove.co.uk",
    "https://www.trustpilot.com/review/rugette.co.uk",
    "https://www.trustpilot.com/review/rugsoflondon.com",
    "https://www.trustpilot.com/review/the-rugs.com",
    "https://www.trustpilot.com/review/naturalrugstore.co.uk",
    "https://www.trustpilot.com/review/modernrugs.co.uk",
    "https://www.trustpilot.com/review/rugstoreonline.co.uk",
    "https://www.trustpilot.com/review/love-rugs.com",
    "https://www.trustpilot.com/review/ruggable.co.uk",
    "https://www.trustpilot.com/review/therugcompany.com",
    "https://www.trustpilot.com/review/homescapes-online.com",
    "https://www.trustpilot.com/review/coxandcox.co.uk",
]

# ─────────────────────────────────────────────
# SCRAPER
# ─────────────────────────────────────────────

RUN_URL = f"https://api.apify.com/v2/acts/{ACTOR_ID}/run-sync-get-dataset-items?token={APIFY_API_TOKEN}&timeout=300&maxTotalChargeUsd={MAX_TOTAL_CHARGE_USD}"
HEADERS = {"Content-Type": "application/json"}


def run():
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")

    print(f"\nTrustpilot Scraper")
    print(f"  Date range: {start_date} -> {end_date}")
    print(f"  Companies:  {len(COMPANIES)}")
    print(f"  Stars:      1-3 only\n")

    payload = {
        "startUrls": [{"url": url} for url in COMPANIES],
        "startDate": start_date,
        "endDate": end_date,
        "maxItems": 10000,
        "filterStars": ["1", "2", "3"],
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }

    response = requests.post(RUN_URL, headers=HEADERS, json=payload, timeout=600)

    if response.status_code not in (200, 201):
        print(f"Error {response.status_code}: {response.text[:300]}")
        return

    reviews = response.json()
    print(f"✓ {len(reviews)} reviews collected")

    timestamp = datetime.today().strftime("%Y%m%d_%H%M%S")
    filename = f"trustpilot_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved: {filename}")


if __name__ == "__main__":
    run()