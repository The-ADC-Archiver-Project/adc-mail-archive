import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE = "https://www.freelists.org/archive/adc"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

def get_soup(url):
    r = session.get(url, timeout=30)
    return BeautifulSoup(r.text, "html.parser")

def extract_post_links(soup):
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/post/adc/" in href:
            links.add(urljoin("https://www.freelists.org", href))

    return links

def extract_month_links(soup):
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/archive/adc/" in href and href != "/archive/adc":
            links.add(urljoin("https://www.freelists.org", href))

    return links

def get_full_post(url):
    soup = get_soup(url)
    text = soup.get_text("\n")
    return text.strip()

def get_title(soup):
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    return "no title"

all_posts = set()
to_visit = set([BASE])
visited = set()

while to_visit:
    url = to_visit.pop()
    if url in visited:
        continue

    visited.add(url)

    try:
        soup = get_soup(url)
    except Exception:
        continue

    posts = extract_post_links(soup)
    all_posts.update(posts)

    months = extract_month_links(soup)
    to_visit.update(months)

print("FOUND POSTS:", len(all_posts))

items = []

for link in all_posts:
    try:
        soup = get_soup(link)
        items.append({
            "title": get_title(soup),
            "content": soup.get_text("\n"),
            "link": link
        })
    except Exception:
        continue

with open("data/feed_raw.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)

print("DONE ITEMS:", len(items))