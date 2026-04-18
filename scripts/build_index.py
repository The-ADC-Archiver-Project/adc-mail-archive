import json
import re
import os

def get_thread_key(title):
    title = title.lower()
    title = re.sub(r"(\bre:\s*)+", "", title, flags=re.IGNORECASE)
    title = re.sub(r"^\[[^\]]+\]\s*", "", title)
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip()

# 🔹 laad nieuwe RSS data
with open("feed_raw.json", "r", encoding="utf-8") as f:
    new_data = json.load(f)

# 🔹 laad bestaande archive (indien bestaat)
existing_items = []

if os.path.exists("feed.json"):
    with open("feed.json", "r", encoding="utf-8") as f:
        old_threads = json.load(f)

        for thread in old_threads:
            for item in thread["items"]:
                existing_items.append(item)

# 🔹 combineer alles
all_items = existing_items.copy()

# 🔹 dedup op link
existing_links = set(item["link"] for item in existing_items)

for item in new_data:
    if item["link"] not in existing_links:
        all_items.append(item)

# 🔹 rebuild threads
threads = {}

for item in all_items:
    title = item["title"]
    content = item["content"]
    link = item["link"]

    thread_key = get_thread_key(title)

    if thread_key not in threads:
        threads[thread_key] = {
            "thread": thread_key,
            "count": 0,
            "items": []
        }

    threads[thread_key]["items"].append({
        "title": title,
        "content": content,
        "link": link
    })

    threads[thread_key]["count"] += 1

# 🔹 save
with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(list(threads.values()), f, indent=2, ensure_ascii=False)