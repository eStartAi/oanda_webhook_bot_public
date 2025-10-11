example_env = """
# ========== MODE ==========
DEFAULT_BROKER=oanda        # Options: oanda, oanda_live, kraken
DRY_RUN=True                # Set to False to enable real trades

# ========== OANDA ==========
OANDA_API_TOKEN=your_oanda_api_key
OANDA_ACCOUNT_ID=your_oanda_account_id
OANDA_ENV=practice          # practice or live
OANDA_BASE_URL=https://api-fxpractice.oanda.com/v3

# ========== KRAKEN ==========
KRAKEN_API_KEY=your_kraken_api_key
KRAKEN_API_SECRET=your_kraken_api_secret
KRAKEN_BASE_URL=https://api.kraken.com

# ========== STRATEGY ==========
MAX_RISK_PER_TRADE=0.01
DEFAULT_TP_PIPS=10
DEFAULT_SL_PIPS=5
POSITION_SIZE_TYPE=percent
FIXED_TRADE_SIZE=1000

# ========== TELEGRAM ==========
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_USER_ID=your_telegram_user_id

# ========== SECURITY ==========
WEBHOOK_SECRET=your_webhook_secret

# ========== LOGGING ==========
LOG_LEVEL=INFO
""".strip()

with open(".env.example", "w") as f:
    f.write(example_env + "\n")

print("✅ .env.example created successfully.")
