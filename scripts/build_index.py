import json
import re

def extract_tags(title):
    tags = re.findall(r"\[[^\]]+\]", title)
    seen = []
    for t in tags:
        t = t.upper()
        if t not in seen:
            seen.append(t)
    return seen

def strip_tags(title):
    return re.sub(r"\[[^\]]+\]", "", title).strip()

def get_key(title):
    t = strip_tags(title)
    t = re.sub(r"(\bre:\s*)+", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t)
    return t.lower().strip()

with open("data/feed_raw.json", "r", encoding="utf-8") as f:
    items = json.load(f)

threads = {}

for item in items:
    title = item["title"]
    content = item["content"]
    link = item["link"]

    key = get_key(title)

    if key not in threads:
        threads[key] = {
            "thread": strip_tags(title),
            "tags": extract_tags(title),
            "count": 0,
            "items": []
        }

    threads[key]["items"].append(item)
    threads[key]["count"] += 1

result = list(threads.values())

with open("data/feed.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)