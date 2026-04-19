import json

with open("data/archive.json", "r", encoding="utf-8") as f:
    data = json.load(f)

count = sum(len(m["posts"]) for m in data["months"])

with open("data/feed.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("INDEX BUILT:", count)