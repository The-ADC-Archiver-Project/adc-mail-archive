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
            print(pr.text[:2000])
            psoup = BeautifulSoup(pr.text, "html.parser")

            # Afzender, ontvanger, datum
            body_parts = []
            for label in ["From", "To", "Date"]:
                tag = psoup.find(text=label)
                if tag and tag.parent:
                    val = tag.parent.find_next_sibling()
                    if val:
                        body_parts.append(f"{label}: {val.get_text(strip=True)}")

            # Mail body uit <pre> tag
            pre = psoup.find("pre")
            if pre:
                body_parts.append("\n" + pre.get_text("\n", strip=True))

            text = "\n".join(body_parts)

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