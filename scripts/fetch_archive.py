import requests
from bs4 import BeautifulSoup
import json

BASE = "https://www.freelists.org/archive/adc"

def get_pages():
    r = requests.get(BASE)
    soup = BeautifulSoup(r.text, "html.parser")

    pages = set()

    for a in soup.find_all("a"):
        href = a.get("href", "")
        if "/archive/adc/" in href:
            if href.startswith("http"):
                pages.add(href)
            else:
                pages.add("https://www.freelists.org" + href)

    return list(pages)

def get_messages(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    out = []

    for a in soup.find_all("a"):
        href = a.get("href", "")
        if "/post/adc/" in href:
            out.append({
                "title": a.text.strip(),
                "link": "https://www.freelists.org" + href
            })

    return out

def get_full(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text("\n").strip()

all_items = []

for page in get_pages():
    for msg in get_messages(page):
        all_items.append({
            "title": msg["title"],
            "content": get_full(msg["link"]),
            "link": msg["link"]
        })

with open("data/feed_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_items, f, indent=2, ensure_ascii=False)