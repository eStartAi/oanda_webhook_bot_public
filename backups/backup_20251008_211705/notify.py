import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_USER_ID")
msg = os.getenv("TELEGRAM_MESSAGE", "📣 Alert from ScaleViper")

if not token or not chat_id:
    print("⚠️ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_USER_ID in .env")
    exit(1)

try:
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={
        "chat_id": chat_id,
        "text": msg
    })
    if r.status_code == 200:
        print("✅ Telegram notification sent.")
    else:
        print(f"⚠️ Telegram API error: {r.text}")
except Exception as e:
    print(f"❌ Failed to send Telegram message: {e}")
