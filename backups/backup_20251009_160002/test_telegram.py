<<<<<<< HEAD
import os
from dotenv import load_dotenv

# ✅ Load the .env file manually
load_dotenv()

# ✅ Now we can import and use the notify function
from utils.notify import telegram_notify

telegram_notify("✅ Telegram is working! This is a test message.")
=======
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MESSAGE = "✅ Telegram bot is working! — ScaleViper Test"

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    print("📤 Sent:", response.json())

if TOKEN and CHAT_ID:
    send_telegram_message(TOKEN, CHAT_ID, MESSAGE)
else:
    print("❌ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found in .env")
>>>>>>> 9504e00 (🔄 Auto-sync 2025-10-01 07:39:17)
