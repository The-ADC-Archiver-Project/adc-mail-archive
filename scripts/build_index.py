import json
import re

def clean_key(title):
    t = re.sub(r"\[[^\]]+\]", "", title)
    t = re.sub(r"re:\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+", " ", t)
    return t.lower().strip()

def extract_tags(title):
    return list(dict.fromkeys(re.findall(r"\[([^\]]+)\]", title.upper())))

with open("data/feed_raw.json", "r", encoding="utf-8") as f:
    items = json.load(f)

threads = {}

for item in items:
    key = clean_key(item["title"])

    if key not in threads:
        threads[key] = {
            "thread": item["title"],
            "tags": extract_tags(item["title"]),
            "count": 0,
            "items": []
        }

    threads[key]["items"].append(item)
    threads[key]["count"] += 1

with open("data/feed.json", "w", encoding="utf-8") as f:
    json.dump(list(threads.values()), f, indent=2, ensure_ascii=False)