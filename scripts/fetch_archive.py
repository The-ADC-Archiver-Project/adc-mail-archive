import requests
from bs4 import BeautifulSoup
import json

BASE = "https://www.freelists.org/archive/adc"

def get_month_pages():
    r = requests.get(BASE)
    soup = BeautifulSoup(r.text, "html.parser")

    pages = []

    for a in soup.find_all("a"):
        href = a.get("href", "")

        if "archive/adc/" in href and len(href.split("/")) > 3:
            if href.startswith("http"):
                pages.append(href)
            else:
                pages.append("https://www.freelists.org" + href)

    return list(set(pages))

def get_messages(month_url):
    r = requests.get(month_url)
    soup = BeautifulSoup(r.text, "html.parser")

    msgs = []

    for a in soup.find_all("a"):
        href = a.get("href", "")
        text = a.text.strip()

        if "/post/adc/" in href and text.startswith("»"):
            if not href.startswith("http"):
                href = "https://www.freelists.org" + href

            msgs.append({
                "title": text.replace("»", "").strip(),
                "link": href
            })

    return msgs

def get_full(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text("\n").strip()

all_items = []

for month in get_month_pages():
    try:
        for msg in get_messages(month):
            all_items.append({
                "title": msg["title"],
                "content": get_full(msg["link"]),
                "link": msg["link"]
            })
    except Exception as e:
        print("error month:", month, e)

with open("data/feed_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_items, f, indent=2, ensure_ascii=False)