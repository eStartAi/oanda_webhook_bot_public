import os
import sqlite3
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import oandapyV20
import oandapyV20.endpoints.orders as orders
from datetime import datetime

# Load environment
load_dotenv()
API_KEY = os.getenv("OANDA_API_TOKEN")
ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
BROKER = os.getenv("DEFAULT_BROKER", "oanda_practice")

app = Flask(__name__)

# DB setup
DB_FILE = "trade_logs.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    side TEXT,
    price REAL,
    units INTEGER,
    sl REAL,
    tp REAL,
    trail REAL,
    status TEXT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# OANDA client
if not API_KEY or not ACCOUNT_ID:
    raise EnvironmentError("Missing OANDA_API_TOKEN or OANDA_ACCOUNT_ID in .env")
client = oandapyV20.API(access_token=API_KEY)

# Helper: calculate position size
def calc_units(balance, risk_pct, stop_loss_pips, pip_value=10):
    risk_amount = balance * (risk_pct / 100)
    units = int(risk_amount / (stop_loss_pips * pip_value))
    return max(units, 1)

# Helper: get account balance
def get_balance():
    try:
        from oandapyV20.endpoints.accounts import AccountSummary
        r = AccountSummary(ACCOUNT_ID)
        client.request(r)
        return float(r.response["account"]["balance"])
    except Exception:
        return 10000.0  # fallback for practice

# Validation
def validate_alert(data):
    required = ["symbol", "side", "price", "key"]
    for field in required:
        if field not in data:
            return False, f"Missing field: {field}"

    if data["key"] != WEBHOOK_SECRET:
        return False, "Invalid webhook secret"

    # sanity check
    try:
        price = float(data["price"])
        if price <= 0:
            return False, "Invalid price"
    except ValueError:
        return False, "Price not numeric"

    return True, "ok"

@app.route("/")
def home():
    return jsonify({
        "service": "OANDA Webhook Bot",
        "status": "ok",
        "account_id": ACCOUNT_ID,
        "trade_logs_count": cur.execute("SELECT COUNT(*) FROM trades").fetchone()[0]
    })

@app.route("/dashboard")
def dashboard():
    rows = cur.execute("SELECT symbol, side, price, units, sl, tp, status, created FROM trades ORDER BY id DESC LIMIT 10").fetchall()
    trades = [dict(zip(["symbol", "side", "price", "units", "sl", "tp", "status", "created"], row)) for row in rows]
    return jsonify({"recent_trades": trades})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📩 Webhook Received:", data)

    valid, msg = validate_alert(data)
    if not valid:
        return jsonify({"status": "error", "message": msg}), 400

    symbol = data["symbol"]
    side = data["side"].lower()
    price = float(data["price"])
    trail = float(data.get("trail", 0.0))

    balance = get_balance()
    stop_loss_pips = 20  # placeholder
    units = calc_units(balance, 1, stop_loss_pips)

    sl = round(price - 0.0020, 5) if side == "buy" else round(price + 0.0020, 5)
    tp = round(price + 0.0050, 5) if side == "buy" else round(price - 0.0050, 5)

    # Save to DB
    cur.execute("INSERT INTO trades (symbol, side, price, units, sl, tp, trail, status) VALUES (?,?,?,?,?,?,?,?)",
                (symbol, side, price, units, sl, tp, trail, "PENDING"))
    conn.commit()
    print(f"✅ Alert saved to DB: {symbol} {side} at {price}")

    # OANDA order
    order = {
        "order": {
            "instrument": symbol,
            "units": str(units if side == "buy" else -units),
            "type": "MARKET",
            "timeInForce": "FOK",
            "positionFill": "DEFAULT",
            "takeProfitOnFill": {"price": str(tp)},
            "stopLossOnFill": {"price": str(sl)}
        }
    }

    try:
        r = orders.OrderCreate(ACCOUNT_ID, data=order)
        client.request(r)
        cur.execute("UPDATE trades SET status=? WHERE id=(SELECT MAX(id) FROM trades)", ("EXECUTED",))
        conn.commit()
        print("✅ Trade Executed:", r.response)
        return jsonify({"status": "ok", "response": r.response})
    except Exception as e:
        cur.execute("UPDATE trades SET status=? WHERE id=(SELECT MAX(id) FROM trades)", ("FAILED",))
        conn.commit()
        print("❌ Error executing trade:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/auto_close")
def auto_close():
    return jsonify({"status": "stub", "message": "Auto-close not yet implemented"})

if __name__ == "__main__":
    print("🚀 Starting Bot on port 5001...")
    app.run(host="0.0.0.0", port=5001)
