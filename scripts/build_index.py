import json
import re

def extract_tags(title):
    tags = re.findall(r"\[([^\]]+)\]", title)
    seen = []
    for t in tags:
        t = t.upper().strip()
        if t not in seen:
            seen.append(t)
    return seen

def strip_tags(title):
    return re.sub(r"\[[^\]]+\]", "", title).strip()

def clean_key(title):
    t = strip_tags(title)
    t = re.sub(r"(?i)\bre:\s*", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.lower().strip()

with open("data/feed_raw.json", "r", encoding="utf-8") as f:
    items = json.load(f)

if not items:
    print("NO RAW DATA")
    with open("data/feed.json", "w") as f:
        json.dump([], f)
    exit(0)

threads = {}

for item in items:
    title = item.get("title", "")
    key = clean_key(title)

    if not key:
        continue

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
result.sort(key=lambda x: x["count"], reverse=True)

with open("data/feed.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"built {len(result)} threads from {len(items)} items")