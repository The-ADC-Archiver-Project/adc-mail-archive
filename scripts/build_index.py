import os
import json
import re

OUTPUT_DIR = "output"

threads = {}

def clean_subject(subject):
    subject = subject.lower()
    subject = re.sub(r"re:\s*", "", subject)
    return subject.strip()

for file in os.listdir(OUTPUT_DIR):
    if not file.endswith(".md"):
        continue

    path = os.path.join(OUTPUT_DIR, file)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    title = lines[0].replace("#", "").strip()

    subject = clean_subject(title)

    if subject not in threads:
        threads[subject] = []

    threads[subject].append({
        "title": title,
        "file": f"output/{file}",
        "content": content
    })

feed = []

for subject, items in threads.items():
    feed.append({
        "thread": subject,
        "count": len(items),
        "items": items
    })

with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(feed, f, indent=2)

print("threaded index built")