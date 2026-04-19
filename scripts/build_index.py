import json
import re
import os

def get_thread_key(title):
    t = title.lower()
    t = re.sub(r"(\bre:\s*)+", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^\[[^\]]+\]\s*", "", t)
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def extract_tag(title):
    match = re.match(r"^\[([^\]]+)\]", title)
    if match:
        return f"[{match.group(1).upper()}]"
    return ""

# 🔹 load RSS
with open("feed_raw.json", "r", encoding="utf-8") as f:
    new_data = json.load(f)

# 🔹 load existing archive
existing_items = []

if os.path.exists("feed.json"):
    with open("feed.json", "r", encoding="utf-8") as f:
        old_threads = json.load(f)
        for thread in old_threads:
            for item in thread["items"]:
                existing_items.append(item)

# 🔹 deduplicate
existing_links = set(item["link"] for item in existing_items)
all_items = existing_items.copy()

for item in new_data:
    if item["link"] not in existing_links:
        all_items.append(item)

# 🔹 build threads
threads = {}

for item in all_items:
    title = item["title"]
    content = item["content"]
    link = item["link"]

    thread_key = get_thread_key(title)
    tag = extract_tag(title)

    if thread_key not in threads:
        threads[thread_key] = {
            "thread": thread_key,
            "tag": tag,
            "count": 0,
            "items": []
        }

    threads[thread_key]["items"].append({
        "title": title,
        "content": content,
        "link": link
    })

    threads[thread_key]["count"] += 1

# 🔥 sort mails binnen thread (nieuwste eerst)
for thread in threads.values():
    thread["items"] = list(reversed(thread["items"]))

# 🔥 sort threads (nieuwste eerst)
sorted_threads = sorted(
    threads.values(),
    key=lambda t: t["items"][0]["link"],  # werkt omdat RSS newest first is
    reverse=True
)

# 🔹 save
with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(sorted_threads, f, indent=2, ensure_ascii=False)