import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_ENABLED = os.getenv("ENABLE_TELEGRAM_ALERTS", "true").lower() == "true"

def send_telegram(message: str):
    if not TELEGRAM_ENABLED:
        return

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Missing Telegram credentials")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"❌ Telegram failed: {response.text}")
    except Exception as e:
        print(f"❌ Exception while sending Telegram alert: {e}")
