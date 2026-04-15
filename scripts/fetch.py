import feedparser
import os

RSS_URL = "https://freelists.org/feed/adc"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

feed = feedparser.parse(RSS_URL)

for entry in feed.entries:
    title = entry.get("title", "no-title")
    content = entry.get("summary", "")
    date = entry.get("published", "no-date")

    safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()[:80]
    filename = f"{OUTPUT_DIR}/{safe_title}.md"

    md = f"# {title}\n\n{date}\n\n{content}\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(md)

print("done")