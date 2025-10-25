from flask import Flask, request, jsonify
import os
import logging
from dotenv import load_dotenv
from risk_guard import calculate_position_size, should_continue_trading
from kraken_trade import place_trade
from log_trades import log_trade

load_dotenv()
app = Flask(__name__)

# === Config ===
RUN_MODE = os.getenv("RUN_MODE", "webhook")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
EXCHANGE = os.getenv("EXCHANGE", "kraken")
APP_PORT = int(os.getenv("APP_PORT", 5003))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret")

# === Risk Settings ===
MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", 3))
DAILY_PROFIT_TARGET = float(os.getenv("DAILY_PROFIT_TARGET", 10))
MAX_CONSECUTIVE_LOSSES = int(os.getenv("MAX_CONSECUTIVE_LOSSES", 2))

# === Logger Setup ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    if data.get("secret") != WEBHOOK_SECRET:
        logging.warning("❌ Unauthorized webhook attempt.")
        return jsonify({"error": "Invalid secret"}), 403

    try:
        symbol = data.get("pair") or data.get("symbol")
        side = data.get("side")
        price = float(data.get("price", 0))
        score = float(data.get("score", 0))
        balance = float(data.get("balance", 1000))  # Default for now
        stop_loss_pct = float(os.getenv("DEFAULT_SL_PCT", 2)) / 100

        size = calculate_position_size(balance, score, price, stop_loss_pct)

        # 🚫 Sanity check before proceeding
        if not symbol or price == 0 or size == 0:
            logging.warning(f"⚠️ Invalid trade input — Symbol: {symbol}, Price: {price}, Size: {size}")
            return jsonify({"error": "Size is 0.0 — skipping trade"}), 400

        logging.info(f"📩 Webhook received: {symbol} {side.upper()} | Score: {score}/10 | Price: {price} | Size: {size}")

        # 🛡️ Risk checks
        allowed, reason = should_continue_trading({})
        if not allowed:
            logging.warning(f"🛑 Trade blocked by risk logic: {reason}")
            return jsonify({"error": reason}), 400

        if DRY_RUN:
            logging.info(f"🧪 DRY_RUN: Simulated {side.upper()} {symbol} @ {price} (size={size}, score={score})")
            trade_result = {
                "status": "dry_run",
                "symbol": symbol,
                "side": side,
                "price": price,
                "size": size,
                "score": score
            }
        else:
            trade_result = place_trade(symbol, side, price, size)

        log_trade(trade_result)

        return jsonify({"response": trade_result})

    except Exception as e:
        logging.error(f"💥 Error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# === App Entry ===
if __name__ == "__main__":
    if RUN_MODE == "auto":
        logging.info("🔁 Auto mode not yet implemented.")
    elif RUN_MODE in ("webhook", "sandbox"):
        if RUN_MODE == "sandbox":
            logging.warning("⚠️ Sandbox mode active — forcing DRY_RUN = True")
            DRY_RUN = True
        logging.info(f"🚀 ScaleViper Webhook Mode starting on port {APP_PORT} (Exchange={EXCHANGE}, DRY_RUN={DRY_RUN})")
        app.run(host="0.0.0.0", port=APP_PORT)
    else:
        logging.error("❌ Invalid RUN_MODE. Use 'auto', 'webhook', or 'sandbox'.")
