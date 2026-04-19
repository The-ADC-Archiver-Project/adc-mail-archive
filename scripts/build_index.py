import json
import re
import os

def normalize_title(title):
    t = title.lower()
    t = re.sub(r"(\bre:\s*)+", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\[[^\]]+\]", "", t)  # verwijder ALLE tags
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def extract_tags(title):
    return " ".join(re.findall(r"\[[^\]]+\]", title))

# 🔹 load RSS
with open("feed_raw.json", "r", encoding="utf-8") as f:
    new_data = json.load(f)

# 🔹 load bestaande archive
existing_items = []

if os.path.exists("feed.json"):
    with open("feed.json", "r", encoding="utf-8") as f:
        old_threads = json.load(f)
        for thread in old_threads:
            for item in thread["items"]:
                existing_items.append(item)

# 🔹 deduplicate
existing_links = set(item["link"] for item in existing_items)

# 🔥 NIEUWSTE ITEMS ECHT BOVENAAN
all_items = []

for item in new_data:
    if item["link"] not in existing_links:
        all_items.append(item)

# daarna oude items
all_items.extend(existing_items)

# 🔹 build threads
threads = {}
thread_order = []

for item in all_items:
    title = item["title"]
    content = item["content"]
    link = item["link"]

    key = normalize_title(title)
    tags = extract_tags(title)

    if key not in threads:
        threads[key] = {
            "thread": title,   # 🔥 originele title gebruiken!
            "tags": tags,
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

# 🔹 output volgorde behouden
result = [threads[k] for k in thread_order]

with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)