import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Runtime settings
DRY_RUN = os.getenv("DRY_RUN", "True").lower() == "true"
DEFAULT_SL_PCT = float(os.getenv("DEFAULT_SL_PCT", 2)) / 100
DEFAULT_TP_PCT = float(os.getenv("DEFAULT_TP_PCT", 3)) / 100

# Thresholds
DAILY_PROFIT_TARGET = float(os.getenv("DAILY_PROFIT_TARGET", 7))
MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", 3))
MAX_CONSECUTIVE_LOSSES = int(os.getenv("MAX_CONSECUTIVE_LOSSES", 2))

# Telegram integration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ENABLE_TELEGRAM_ALERTS = os.getenv("ENABLE_TELEGRAM_ALERTS", "false").lower() == "true"

# Watchlist
WATCHLIST = os.getenv("WATCHLIST", "ETH/USD,SOL/USD,MATIC/USD").split(',')
