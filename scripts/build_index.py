import os
import json

DATA_DIR = "data"
RAW_FILE = os.path.join(DATA_DIR, "feed_raw.json")
OUT_FILE = os.path.join(DATA_DIR, "feed.json")

if not os.path.exists(RAW_FILE):
    print("NO RAW DATA")
    exit(0)

with open(RAW_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", [])

index = {
    "count": len(items),
    "items": items
}

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

print("INDEX BUILT:", len(items))