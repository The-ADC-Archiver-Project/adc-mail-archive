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
    tags = re.findall(r"\[[^\]]+\]", title)
    cleaned = []
    for t in tags:
        t = t.strip().upper()
        if t not in cleaned:
            cleaned.append(t)
    return cleaned

def clean_title(title):
    title = re.sub(r"^\[[^\]]+\]\s*", "", title)
    title = re.sub(r"(\bre:\s*)+", "", title, flags=re.IGNORECASE)
    return title.strip()

def normalize_tags(tags):
    if isinstance(tags, str):
        tags = re.findall(r"\[[^\]]+\]", tags)

    cleaned = []
    for t in tags:
        t = t.strip().upper()
        if t not in cleaned:
            cleaned.append(t)
    return cleaned

def load_old_threads():
    if not os.path.exists("feed.json"):
        return {}

    with open("feed.json", "r", encoding="utf-8") as f:
        old = json.load(f)

    fixed = {}

    for thread in old:
        tags = normalize_tags(thread.get("tags", []))

        fixed[thread["thread"].lower()] = {
            "thread": thread["thread"],
            "tags": tags,
            "count": thread["count"],
            "items": thread["items"]
        }

    return fixed


# =========================
# LOAD INPUT
# =========================

with open("feed_raw.json", "r", encoding="utf-8") as f:
    items = json.load(f)

threads = load_old_threads()
order = list(threads.keys())

existing_links = set()

for t in threads.values():
    for item in t["items"]:
        existing_links.add(item["link"])

# =========================
# PROCESS NEW ITEMS
# =========================

for item in items:
    title = item["title"]
    content = item["content"]
    link = item["link"]

    if link in existing_links:
        continue

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
    existing_links.add(link)

# =========================
# OUTPUT
# =========================

result = [threads[k] for k in order]

with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)