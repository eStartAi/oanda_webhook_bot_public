import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv(dotenv_path=".env")

# Kraken-first required environment variables
REQUIRED_ENV = [
    "DEFAULT_BROKER",
    "DRY_RUN",
    "KRAKEN_API_KEY",
    "KRAKEN_API_SECRET",
    "KRAKEN_BASE_URL",
    "DEFAULT_SL_PCT",
    "DEFAULT_TP_PCT",
    "DAILY_PROFIT_TARGET",
    "MAX_DAILY_LOSS",
    "MAX_CONSECUTIVE_LOSSES",
    "WATCHLIST",
    "WEBHOOK_SECRET",
    "LOG_LEVEL",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "ENABLE_TELEGRAM_ALERTS"
]

def validate_env():
    missing = []
    for key in REQUIRED_ENV:
        if not os.getenv(key):
            missing.append(key)

    if missing:
        print("❌ Missing required environment variables:\n")
        for m in missing:
            print(f" - {m}")
        print("\n🛑 Fix your .env file.")
        sys.exit(1)

    print("✅ All required environment variables found.\n")

    # 🎛️ Pretty print summary
    print("=== ⚙️ ScaleViper Environment Summary ===")
    print(f"Broker:           {os.getenv('DEFAULT_BROKER')}")
    print(f"Mode:             {'DRY RUN' if os.getenv('DRY_RUN','true').lower()=='true' else 'LIVE'}")
    print(f"Kraken URL:       {os.getenv('KRAKEN_BASE_URL')}")
    print(f"SL% / TP%:        {os.getenv('DEFAULT_SL_PCT')} / {os.getenv('DEFAULT_TP_PCT')}")
    print(f"Daily Target:     {os.getenv('DAILY_PROFIT_TARGET')}%")
    print(f"Max Daily Loss:   {os.getenv('MAX_DAILY_LOSS')}%")
    print(f"Max Streak Loss:  {os.getenv('MAX_CONSECUTIVE_LOSSES')}")
    print(f"Watchlist:        {os.getenv('WATCHLIST')}")
    print(f"Log Level:        {os.getenv('LOG_LEVEL')}")
    print(f"Telegram Enabled: {os.getenv('ENABLE_TELEGRAM_ALERTS')}")
    print("========================================")

if __name__ == "__main__":
    validate_env()
