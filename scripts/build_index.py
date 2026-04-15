import os
import json

OUTPUT_DIR = "output"

items = []

for file in os.listdir(OUTPUT_DIR):
    if file.endswith(".md"):
        path = os.path.join(OUTPUT_DIR, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        title = content.split("\n")[0].replace("#", "").strip()

        items.append({
            "title": title,
            "file": f"output/{file}",
            "content": content
        })

with open("feed.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2)

print("index built")