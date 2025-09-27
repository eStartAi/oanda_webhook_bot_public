import os
from dotenv import load_dotenv

# ✅ Load the .env file manually
load_dotenv()

# ✅ Now we can import and use the notify function
from utils.notify import telegram_notify

telegram_notify("✅ Telegram is working! This is a test message.")
