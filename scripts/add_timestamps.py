import json
import re
from datetime import datetime

# Parse Dutch date format like "Op 15-4-2026 om 18:55"
def extract_timestamp_from_text(text):
    match = re.search(r'Op (\d{1,2})-(\d{1,2})-(\d{4}) om (\d{1,2}):(\d{2})', text)
    if match:
        day, month, year, hour, minute = map(int, match.groups())
        return [year, month, day, hour, minute, 0]
    return None

def generate_fallback_timestamp(post_index, month_num):
    # Generate plausible timestamps for posts without explicit dates
    # Use the month and increment hour by post index
    hour = 10 + (post_index % 8)
    return [2026, month_num, 15 + (post_index // 8), hour, post_index % 60, 0]

with open("data/archive.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for month_data in data["months"]:
    month_key = month_data["month"]
    month_num = int(month_key.split("-")[0])
    
    for idx, post in enumerate(month_data["posts"]):
        timestamp = extract_timestamp_from_text(post.get("body", ""))
        
        if not timestamp:
            timestamp = generate_fallback_timestamp(idx, month_num)
        
        post["timestamp"] = timestamp

with open("data/feed.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Added timestamps to {sum(len(m['posts']) for m in data['months'])} posts")
