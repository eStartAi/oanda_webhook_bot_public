#!/bin/bash

echo "🛠️ Patching GitHub Action: checklist.yml..."

ACTION_PATH=".github/workflows/checklist.yml"
mkdir -p .github/workflows

cat > "$ACTION_PATH" << 'EOF'
name: Enforce Checklist

on:
  push:
    branches:
      - main
      - live

jobs:
  checklist:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Enforce CHECKLIST.md update (safe HEAD check)
        run: |
          if git rev-parse HEAD~1 >/dev/null 2>&1; then
            if ! git diff --name-only HEAD~1 HEAD | grep -q "^CHECKLIST.md$"; then
              echo "❌ CHECKLIST.md was not updated in the latest commit."
              exit 1
            else
              echo "✅ CHECKLIST.md was updated in this commit."
            fi
          else
            echo "ℹ️ Skipping checklist diff check — likely first commit or no HEAD~1."
          fi
EOF

echo "✅ GitHub Action patched at $ACTION_PATH"

# --------------------------------------

echo "🛠️ Patching notify.py to prevent Telegram parse errors..."

NOTIFY_PATH="notify.py"

cat > "$NOTIFY_PATH" << 'EOF'
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

def escape_markdown_v2(text):
    return re.sub(r'([_\*\[\]\(\)~`>#+\-=|{}.!])', r'\\\1', text)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
RAW_MESSAGE = os.getenv("TELEGRAM_MESSAGE", "📢 Test notification from ScaleViper")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("⚠️ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env")
    exit(1)

MESSAGE = escape_markdown_v2(RAW_MESSAGE)

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "MarkdownV2",
    }

    try:
        print(f"📤 Sending message to Telegram: {RAW_MESSAGE}")
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Telegram response: 200")
        else:
            print(f"❌ Telegram error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception during Telegram send: {e}")

send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, MESSAGE)
EOF

echo "✅ notify.py patched to use safe MarkdownV2 escaping"

echo -e "\n🎉 All patches applied successfully!"
