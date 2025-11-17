import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

# === Risk Settings ===
MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", 3))
DAILY_PROFIT_TARGET = float(os.getenv("DAILY_PROFIT_TARGET", 10))
MAX_CONSECUTIVE_LOSSES = int(os.getenv("MAX_CONSECUTIVE_LOSSES", 2))

TRADE_LOG_PATH = os.path.join(os.path.dirname(__file__), "trade_logs.jsonl")

# === Position Sizing ===
def calculate_position_size(balance, score, price, stop_loss_pct):
    """
    Example position sizing: 1% risk per trade.
    """
    risk_amount = balance * 0.01
    sl_distance = price * stop_loss_pct
    if sl_distance == 0:
        return 0
    size = risk_amount / sl_distance
    return round(size, 4)

# === Trade Continuation Check ===
def should_continue_trading(state):
    """
    Placeholder: always return True.
    """
    return True, "Continue trading"

# === Daily Trade Loader ===
def load_today_trades():
    if not os.path.exists(TRADE_LOG_PATH):
        return []

    today = datetime.utcnow().date()
    trades = []

    with open(TRADE_LOG_PATH, "r") as f:
        for line in f:
            try:
                trade = json.loads(line)
                timestamp = datetime.fromisoformat(trade["timestamp"]).date()
                if timestamp == today:
                    trades.append(trade)
            except:
                continue

    return trades

# === PnL + Streak Calculator ===
def calculate_stats(trades):
    total_profit = 0
    consecutive_losses = 0
    max_consec = 0

    for trade in trades:
        pnl = trade.get("pnl", 0)
        total_profit += pnl

        if pnl < 0:
            consecutive_losses += 1
            max_consec = max(max_consec, consecutive_losses)
        else:
            consecutive_losses = 0

    return total_profit, max_consec

# === ✅ Core RISK GUARD ===
def validate_risk(symbol, side, price, size):
    trades = load_today_trades()
    total_profit, consec_losses = calculate_stats(trades)

    if total_profit < -MAX_DAILY_LOSS:
        print(f"❌ Max daily loss exceeded: {total_profit} < -{MAX_DAILY_LOSS}")
        return False

    if total_profit >= DAILY_PROFIT_TARGET:
        print(f"✅ Daily profit target hit: {total_profit} ≥ {DAILY_PROFIT_TARGET}")
        return False

    if consec_losses >= MAX_CONSECUTIVE_LOSSES:
        print(f"⚠️ Max consecutive losses reached: {consec_losses}")
        return False

    return True
