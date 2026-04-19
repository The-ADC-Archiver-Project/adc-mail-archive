import os
import json
import cloudscraper
from bs4 import BeautifulSoup

URL = "https://www.freelists.org/archive/adc"

DATA_DIR = "data"
RAW_FILE = os.path.join(DATA_DIR, "feed_raw.json")

os.makedirs(DATA_DIR, exist_ok=True)

scraper = cloudscraper.create_scraper()

response = scraper.get(URL)

print("STATUS:", response.status_code)
print("FINAL URL:", response.url)
print("CONTENT TYPE:", response.headers.get("content-type"))

html = response.text

if "Just a moment" in html or response.status_code != 200:
    print("BLOCKED OR FAILED REQUEST")
    data = {
        "months": 0,
        "items": []
    }
else:
    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a")
    items = []

    for a in links:
        href = a.get("href")
        text = a.get_text(strip=True)

        if href and "archive" in href:
            items.append({
                "title": text,
                "url": href
            })

    print("TOTAL ITEMS:", len(items))

    data = {
        "months": len(items),
        "items": items
    }

with open(RAW_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)