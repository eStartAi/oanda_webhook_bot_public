import os, urllib.request, urllib.parse

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def telegram_notify(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }).encode()

    try:
        print(f"📤 Sending message to Telegram: {text}")
        with urllib.request.urlopen(urllib.request.Request(url, data=data)) as r:
            print(f"✅ Telegram response: {r.status}")
            return r.status == 200
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")
        return False
