import imaplib
import email
from email.header import decode_header
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

# Verbind met Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(GMAIL_USER, GMAIL_PASS)
mail.select("inbox")

# Zoek alle mails van de ADC lijst
status, messages = mail.search(None, 'FROM "adc@freelists.org"')

result = {}

for num in messages[0].split():
    status, data = mail.fetch(num, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])

    subject = decode_str(msg["Subject"])
    sender = decode_str(msg["From"])
    date = msg["Date"]
    url = msg.get("X-List-Archive", "")
    body = get_body(msg)

    # Groepeer per maand
    from email.utils import parsedate
    parsed_date = parsedate(date)
    if parsed_date:
        month_key = f"{parsed_date[1]:02d}-{parsed_date[0]}"
    else:
        month_key = "unknown"

    if month_key not in result:
        result[month_key] = []

    result[month_key].append({
        "title": subject,
        "url": url,
        "body": body
    })

mail.logout()

# Bouw de JSON structuur
output = {
    "months": [
        {"month": k, "posts": v}
        for k, v in sorted(result.items(), key=lambda x: x[0])
    ]
}

os.makedirs("data", exist_ok=True)

with open("data/archive.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("DONE, mails gevonden:", sum(len(v) for v in result.values()))