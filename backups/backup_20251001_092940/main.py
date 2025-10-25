from flask import Flask, request, jsonify
<<<<<<< HEAD
import os
import logging
from utils.trade import execute_trade
from utils.risk import validate_risk
from utils.logger import log_trade
=======
from dotenv import load_dotenv
import oandapyV20
import oandapyV20.endpoints.orders as orders
from datetime import datetime

from utils.filters import ai_gate_allow, record_trade
from utils.trade import create_trailing_stop
from dotenv import load_dotenv
load_dotenv()

# Validate .env before continuing
import validate_env

# Load environment
load_dotenv()
API_KEY = os.getenv("OANDA_API_TOKEN")
ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
BROKER = os.getenv("DEFAULT_BROKER", "oanda_practice")
>>>>>>> 9504e00 (🔄 Auto-sync 2025-10-01 07:39:17)

app = Flask(__name__)

# ===========================
# 🔑 Config
# ===========================
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "change_me_secret")
APP_PORT = int(os.getenv("APP_PORT", 5001))
DRY_RUN = int(os.getenv("DRY_RUN", "1")) == 1

EXCHANGE = os.getenv("EXCHANGE", "kraken")  # default = Kraken

# ===========================
# 📝 Logging setup
# ===========================
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scaleviper.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)


@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Accepts incoming trade signals (e.g., from TradingView).
    Expects JSON payload with keys: secret, symbol, side, type, price, size.
    """

    data = request.get_json()

    # 1. Security check
    if data.get("secret") != WEBHOOK_SECRET:
        logging.warning("❌ Unauthorized webhook attempt.")
        return jsonify({"error": "Invalid secret"}), 403

    try:
        symbol = data.get("symbol")
        side = data.get("side")  # buy/sell
        order_type = data.get("type", "market")
        price = float(data.get("price", 0))
        size = float(data.get("size", 0))  # optional fixed size

        logging.info(f"📩 Incoming signal: {data}")

        # 2. Validate risk
        if not validate_risk(symbol, side, price, size):
            logging.warning("⚠️ Risk validation failed.")
            return jsonify({"error": "Risk check failed"}), 400

        # 3. Execute trade
        if DRY_RUN:
            logging.info(f"🧪 DRY_RUN: Simulated {side.upper()} {symbol} @ {price}")
            trade_result = {"status": "dry_run", "symbol": symbol, "side": side, "price": price}
        else:
            trade_result = execute_trade(EXCHANGE, symbol, side, order_type, price, size)

        # 4. Log trade
        log_trade(trade_result)

        return jsonify({"response": trade_result})

    except Exception as e:
        logging.error(f"💥 Error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"🚀 ScaleViper starting on port {APP_PORT} (Exchange={EXCHANGE}, DRY_RUN={DRY_RUN})")
    app.run(host="0.0.0.0", port=APP_PORT)
