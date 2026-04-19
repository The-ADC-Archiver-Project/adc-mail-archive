import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE = "https://www.freelists.org/archive/adc"

def get_all_message_links():
    r = requests.get(BASE, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    links = set()

    for a in soup.find_all("a"):
        href = a.get("href", "")

        if "/post/adc/" in href:
            full = urljoin("https://www.freelists.org", href)
            links.add(full)

    return list(links)

def get_mail(url):
    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.text.strip() if soup.title else url
    content = soup.get_text("\n")

    return {
        "title": title,
        "content": content,
        "link": url
    }

def main():
    items = []

    for url in get_all_message_links():
        try:
            items.append(get_mail(url))
        except Exception as e:
            print("fail:", url, e)

    with open("data/feed_raw.json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()