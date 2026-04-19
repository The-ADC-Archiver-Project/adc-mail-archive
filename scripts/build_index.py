import json
import re
import os

def get_thread_key(title):
    t = title.lower()
    t = re.sub(r"(\bre:\s*)+", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^\[[^\]]+\]\s*", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def extract_tags(title):
    return re.findall(r"\[[^\]]+\]", title)

def clean_title(title):
    title = re.sub(r"(\bre:\s*)+", "", title, flags=re.IGNORECASE)
    return title.strip()

with open("feed_raw.json", "r", encoding="utf-8") as f:
    new_data = json.load(f)

existing_items = []

if os.path.exists("feed.json"):
    with open("feed.json", "r", encoding="utf-8") as f:
        old_threads = json.load(f)
        for thread in old_threads:
            for item in thread["items"]:
                existing_items.append(item)

existing_links = set(item["link"] for item in existing_items)

all_items = []
for item in new_data:
    if item["link"] not in existing_links:
        all_items.append(item)

all_items.extend(existing_items)

threads = {}
thread_order = []

for item in all_items:
    title = item["title"]
    content = item["content"]
    link = item["link"]

    key = get_thread_key(title)

    if key not in threads:
        # 🔥 TAGS ONLY ONCE (IMPORTANT FIX)
        tags = extract_tags(title)

        threads[key] = {
            "thread": clean_title(title),
            "tags": " ".join(tags),   # NO duplication possible anymore
            "count": 0,
            "items": []
        }
        thread_order.append(key)

    threads[key]["items"].append({
        "title": title,
        "content": content,
        "link": link
    })

    threads[key]["count"] += 1

result = [threads[k] for k in thread_order]

with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)