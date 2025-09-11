from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import sqlite3

# Load env vars
load_dotenv()
API_TOKEN = os.getenv("OANDA_API_TOKEN")
ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = Flask(__name__)

# Ensure DB exists
db = sqlite3.connect("trade_logs.db", check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS trades (id INTEGER PRIMARY KEY, symbol TEXT, side TEXT, price REAL, ts DATETIME DEFAULT CURRENT_TIMESTAMP)")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📩 Webhook Received:", data)

    if data.get("key") != WEBHOOK_SECRET:
        return jsonify({"status": "unauthorized"}), 403

    symbol, side, price = data.get("symbol"), data.get("side"), data.get("price")
    db.execute("INSERT INTO trades (symbol, side, price) VALUES (?, ?, ?)", (symbol, side, price))
    db.commit()

    return jsonify({"status": "ok", "message": f"Saved {side} {symbol} at {price}"}), 200

if __name__ == "__main__":
    print("🚀 Starting Webhook Bot...")
    app.run(host="0.0.0.0", port=5001)
