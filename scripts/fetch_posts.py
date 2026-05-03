import imaplib
import email
from email.header import decode_header
from email.utils import parsedate
import json
import os

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_PASS = os.environ["GMAIL_PASS"]

def decode_str(s):
    if s is None:
        return ""
    parts = decode_header(s)
    result = ""
    for part, enc in parts:
        if isinstance(part, bytes):
            result += part.decode(enc or "utf-8", errors="replace")
        else:
            result += part
    return result

def get_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    body += payload.decode(part.get_content_charset() or "utf-8", errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode(msg.get_content_charset() or "utf-8", errors="replace")
    return body.strip()

# Laad bestaande archive in (als die bestaat)
os.makedirs("data", exist_ok=True)
archive_path = "data/archive.json"

existing = {}
if os.path.exists(archive_path):
    with open(archive_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for m in data["months"]:
        existing[m["month"]] = {p["title"]: p for p in m["posts"]}

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(GMAIL_USER, GMAIL_PASS)
mail.select("inbox")

status, messages = mail.search(None, 'FROM "dmarc-noreply@freelists.org"')

print("Gevonden:", len(messages[0].split()))

new_posts = {}

for num in messages[0].split():
    status, data = mail.fetch(num, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])

    subject = decode_str(msg["Subject"])
    date = msg["Date"]
    url = msg.get("X-List-Archive", "")
    body = get_body(msg)

    parsed_date = parsedate(date)
    if parsed_date:
        month_key = f"{parsed_date[1]:02d}-{parsed_date[0]}"
    else:
        month_key = "unknown"

    if month_key not in new_posts:
        new_posts[month_key] = {}

    new_posts[month_key][subject] = {
        "title": subject,
        "url": url,
        "body": body
    }

mail.logout()

# Samenvoegen: bestaande data + nieuwe data
merged = {}

all_keys = set(existing.keys()) | set(new_posts.keys())
for key in all_keys:
    merged[key] = {}
    if key in existing:
        merged[key].update(existing[key])
    if key in new_posts:
        merged[key].update(new_posts[key])  # nieuwe posts overschrijven/voegen toe

output = {
    "months": [
        {"month": k, "posts": list(v.values())}
        for k, v in sorted(merged.items(), key=lambda x: (int(x[0].split("-")[1]), int(x[0].split("-")[0])))
    ]
}

with open(archive_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

total = sum(len(v) for v in merged.values())
print("DONE, totaal mails in archive:", total)