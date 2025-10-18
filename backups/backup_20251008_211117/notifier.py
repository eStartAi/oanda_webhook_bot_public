def send_telegram_message(msg):
    print(f"📲 Telegram message: {msg}")

def build_daily_summary(state):
    balance = state.get("current_balance", 0)
    return f"Daily summary: balance = {balance:.2f}"
