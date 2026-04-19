import cloudscraper
from bs4 import BeautifulSoup
import json
import os

scraper = cloudscraper.create_scraper()

with open("data/index.json", "r", encoding="utf-8") as f:
    index = json.load(f)

result = {"months": []}

for month in index["months"]:
    url = month["url"]

    r = scraper.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    posts = []

    for a in soup.find_all("a"):
        href = a.get("href", "")
        title = a.text.strip()

        if "/post/adc/" in href:
            full_url = "https://www.freelists.org" + href

            pr = scraper.get(full_url)
            psoup = BeautifulSoup(pr.text, "html.parser")

            text = psoup.get_text("\n", strip=True)

            posts.append({
                "title": title,
                "url": full_url,
                "body": text
            })

    result["months"].append({
        "month": month["month"],
        "posts": posts
    })

os.makedirs("data", exist_ok=True)

with open("data/archive.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("DONE")