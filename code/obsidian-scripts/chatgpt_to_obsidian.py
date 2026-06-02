import json
from datetime import datetime
from pathlib import Path
import re

# ---- CONFIG ----
EXPORT_FILE = Path.home() / "Downloads/ChatGPT/conversations.json"
OUTPUT_DIR = Path("~/Downloads/ChatGPT/notes").expanduser()
OUTPUT_DIR.mkdir(exist_ok=True)

def sanitize_filename(text):
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", " ", text).strip()

with open(EXPORT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for convo in data:
    convo_id = convo.get("id")
    title = convo.get("title", "Untitled Chat")
    created = convo.get("create_time")

    date = datetime.fromtimestamp(created).strftime("%Y-%m-%d") if created else "unknown-date"
    filename = f"{date} – {sanitize_filename(title)}.md"
    filepath = OUTPUT_DIR / filename

    messages = convo.get("mapping", {})

    reasoning_blocks = []

    for msg in messages.values():
        message = msg.get("message")
        if not message:
            continue

        role = message.get("author", {}).get("role")
        parts = message.get("content", {}).get("parts", [])
        print(f"Parts structure: {parts[:2]}")

        if role in ("user", "assistant") and parts:
            text_parts = []
            for part in parts:
                if isinstance(part, str):
                    text_parts.append(part)
                elif isinstance(part, dict):
                    # Handle different content types
                    if part.get("content_type") == "text":
                        text_parts.append(part.get("text", ""))
                    elif part.get("content_type") == "image_asset_pointer":
                        text_parts.append("[Image]")
                    # Add other content types as needed

            if text_parts:  # Only add if there's actual text content
                text = "\n".join(text_parts)
                reasoning_blocks.append(f"### {role.capitalize()}\n{text}\n")

    md = f"""---
type: chatgpt
date: {date}
source: ChatGPT
model: unknown
confidence: draft
domains: []
audience: []
reusable: false
conversation_id: {convo_id}
---

## Executive Summary
<!-- Write a 3–4 line human summary -->

## Reusable Output
<!-- Curate clean, copy-paste-ready content -->

## Alternatives Considered
<!-- Optional -->

## Assumptions & Constraints
<!-- Optional -->

## ChatGPT Reasoning (Reference Only)
> ⚠️ Raw AI conversation. Not reusable as-is.

{chr(10).join(reasoning_blocks)}
"""

    filepath.write_text(md, encoding="utf-8")

print("✅ Conversion complete.")