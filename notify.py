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
