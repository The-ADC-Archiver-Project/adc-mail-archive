import feedparser
import json

RSS_URL = "https://freelists.org/feed/adc"

feed = feedparser.parse(RSS_URL)

items = []

for entry in feed.entries:
    items.append({
        "title": entry.get("title", ""),
        "content": entry.get("summary", ""),
        "link": entry.get("link", "")
    })

with open("feed_raw.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)