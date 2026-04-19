import requests
from bs4 import BeautifulSoup
import json

BASE = "https://www.freelists.org/archive/adc"

def get_archive_pages():
    r = requests.get(BASE)
    soup = BeautifulSoup(r.text, "html.parser")

    pages = set()

    for a in soup.find_all("a"):
        href = a.get("href", "")
        if "archive/adc" in href and href != "/archive/adc":
            if href.startswith("http"):
                pages.add(href)
            else:
                pages.add("https://www.freelists.org" + href)

    return list(pages)

def get_messages(page_url):
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text, "html.parser")

    messages = []

    for a in soup.find_all("a"):
        href = a.get("href", "")
        text = a.text.strip()

        if "/post/adc/" in href:
            messages.append({
                "title": text,
                "link": "https://www.freelists.org" + href
            })

    return messages

def get_full_mail(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text("\n")

    return text.strip()

all_pages = get_archive_pages()

all_items = []

for page in all_pages:
    messages = get_messages(page)

    for msg in messages:
        full = get_full_mail(msg["link"])

        all_items.append({
            "title": msg["title"],
            "content": full,
            "link": msg["link"]
        })

with open("data/feed_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_items, f, indent=2, ensure_ascii=False)