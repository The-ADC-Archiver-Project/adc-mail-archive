import cloudscraper
from bs4 import BeautifulSoup
import json
import os

scraper = cloudscraper.create_scraper()

URL = "https://www.freelists.org/archive/adc"

r = scraper.get(URL)
soup = BeautifulSoup(r.text, "html.parser")

months = []

for a in soup.find_all("a"):
    href = a.get("href", "")
    text = a.text.strip()

    if "/archive/adc/" in href and text:
        months.append({
            "month": text,
            "url": "https://www.freelists.org" + href
        })

data = {"months": months}

os.makedirs("data", exist_ok=True)

with open("data/index.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("MONTHS FOUND:", len(months))