import requests
from bs4 import BeautifulSoup
import json
import time

BASE = "https://www.freelists.org/archive/adc"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

def get_month_pages():
    r = requests.get(BASE, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    pages = set()

    for a in soup.select("a[href]"):
        href = a.get("href")

        if not href:
            continue

        if "/archive/adc/" in href:
            if href.startswith("http"):
                pages.add(href)
            else:
                pages.add("https://www.freelists.org" + href)

    return list(pages)

def get_messages(month_url):
    r = requests.get(month_url, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    msgs = []

    for a in soup.select("a[href]"):
        href = a.get("href")
        text = a.text.strip()

        if not href:
            continue

        if "/post/adc/" in href:
            if not href.startswith("http"):
                href = "https://www.freelists.org" + href

            msgs.append({
                "title": text.replace("»", "").strip(),
                "link": href
            })

    return msgs

def get_full(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    return soup.get_text("\n").strip()

all_items = []

months = get_month_pages()
print("MONTHS:", len(months))

for month in months:
    try:
        msgs = get_messages(month)
        print("MSGS:", month, len(msgs))

        for msg in msgs:
            try:
                all_items.append({
                    "title": msg["title"],
                    "content": get_full(msg["link"]),
                    "link": msg["link"]
                })
                time.sleep(0.2)
            except Exception as e:
                print("msg error:", e)

    except Exception as e:
        print("month error:", month, e)

print("TOTAL ITEMS:", len(all_items))

with open("data/feed_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_items, f, indent=2, ensure_ascii=False)