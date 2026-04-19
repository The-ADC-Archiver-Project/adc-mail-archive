import os
import json
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.freelists.org"
INDEX = "https://www.freelists.org/archive/adc"

DATA_DIR = "data"
OUT_FILE = os.path.join(DATA_DIR, "feed_raw.json")

os.makedirs(DATA_DIR, exist_ok=True)

scraper = cloudscraper.create_scraper()

def get_months():
    r = scraper.get(INDEX)
    soup = BeautifulSoup(r.text, "html.parser")

    months = []

    for a in soup.select("a[href]"):
        href = a["href"]

        if "/archive/adc/" in href and href.count("/") >= 3:
            months.append(urljoin(BASE, href))

    return list(set(months))

def get_posts(month_url):
    r = scraper.get(month_url)
    soup = BeautifulSoup(r.text, "html.parser")

    posts = []

    for a in soup.select("a[href]"):
        href = a["href"]
        title = a.get_text(strip=True)

        full_url = urljoin(BASE, href)

        if "/post/adc/" in full_url:
            posts.append({
                "title": title,
                "url": full_url
            })

    return posts

def main():
    months = get_months()

    print("MONTHS FOUND:", len(months))

    result = {
        "months": []
    }

    for m in months:
        month_name = m.rstrip("/").split("/")[-1]

        print("MONTH:", month_name)

        posts = get_posts(m)

        print("POSTS:", len(posts))

        result["months"].append({
            "month": month_name,
            "count": len(posts),
            "posts": posts
        })

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("DONE")

if __name__ == "__main__":
    main()