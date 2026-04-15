import json
import re

with open("feed_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

threads = {}

def get_thread_key(title):
    title = re.sub(r"^(Re:\s*)+", "", title)
    title = re.sub(r"^\[ADC\]\s*", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip().lower()

for item in data:
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

with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(list(threads.values()), f, indent=2, ensure_ascii=False)