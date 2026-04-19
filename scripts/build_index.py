import json
import re

def get_thread_key(title):
    t = title.lower()
    t = re.sub(r"(\bre:\s*)+", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^\[[^\]]+\]\s*", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def extract_tags(title):
    tags = re.findall(r"\[[^\]]+\]", title)
    seen = []
    for t in tags:
        t = t.strip().upper()
        if t not in seen:
            seen.append(t)
    return seen

def clean_title(title):
    title = re.sub(r"^\[[^\]]+\]\s*", "", title)
    title = re.sub(r"(\bre:\s*)+", "", title, flags=re.IGNORECASE)
    return title.strip()

with open("feed_raw.json", "r", encoding="utf-8") as f:
    items = json.load(f)

threads = {}
order = []

for item in items:
    title = item["title"]
    content = item["content"]
    link = item["link"]

    key = get_thread_key(title)

    if key not in threads:
        threads[key] = {
            "thread": clean_title(title),
            "tags": extract_tags(title),
            "count": 0,
            "items": []
        }
        order.append(key)

    threads[key]["items"].append({
        "title": title,
        "content": content,
        "link": link
    })

    threads[key]["count"] += 1

result = [threads[k] for k in order]

with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)