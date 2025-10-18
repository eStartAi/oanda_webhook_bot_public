from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import sqlite3
import subprocess
import requests
from datetime import datetime
import pytz

# === Load environment variables ===
load_dotenv()
API_TOKEN = os.getenv("OANDA_API_TOKEN")
ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# === Telegram Settings ===
BOT_TOKEN = "8403544466:AAGnXAIsi2T7tP8X_TopwjEc5nWV78ijFog"
CHAT_ID = "6988109541"
AUTHORIZED_USERS = ["6988109541"]
TIMEZONE = "US/Eastern"

# === Flask app ===
app = Flask(__name__)

# === SQLite setup ===
db = sqlite3.connect("trade_logs.db", check_same_thread=False)
db.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY,
    symbol TEXT,
    side TEXT,
    price REAL,
    ts DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

db.execute("""
CREATE TABLE IF NOT EXISTS command_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    command TEXT,
    status TEXT,
    ts DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# === Utility: Log command to DB ===
def log_command(user_id, command, status):
    db.execute("INSERT INTO command_logs (user_id, command, status) VALUES (?, ?, ?)",
               (user_id, command, status))
    db.commit()

# === Utility: Telegram trade alert ===
def send_telegram_trade_alert(symbol, side, price):
    now = datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d %I:%M:%S %p")
    message = (
        "💹 *Trade Executed*\n"
        f"Symbol: `{symbol}`\n"
        f"Side: `{side.upper()}`\n"
        f"Price: `{price}`\n"
        f"Time: {now}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

# === Utility: systemctl actions ===
def systemctl_action(action):
    try:
        subprocess.run(["sudo", "systemctl", action, "scanner.service"], check=True)
        return f"✅ scanner.service {action}ed"
    except subprocess.CalledProcessError:
        return f"❌ Failed to {action} scanner.service"

# === In-memory pending confirmation ===
PENDING_ACTIONS = {}

# === ROUTE: TradingView Webhook ===
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data.get("key") != WEBHOOK_SECRET:
        return jsonify({"error": "unauthorized"}), 403

    symbol = data.get("symbol")
    side = data.get("side")
    price = float(data.get("price"))

    db.execute("INSERT INTO trades (symbol, side, price) VALUES (?, ?, ?)", (symbol, side, price))
    db.commit()

    send_telegram_trade_alert(symbol, side, price)
    print(f"📩 Webhook Received: {data}")
    return jsonify({"status": "ok", "message": f"Saved {side} {symbol} at {price}"})


# === ROUTE: Telegram Kill Switch ===
@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.json
    msg = data.get("message", {})
    user_id = str(msg.get("from", {}).get("id"))
    text = msg.get("text", "").lower().strip()

    if user_id not in AUTHORIZED_USERS:
        return jsonify({"ok": False, "message": "Unauthorized user"}), 403

    if text == "/startscanner":
        log_command(user_id, text, "executed")
        return jsonify({"ok": True, "message": systemctl_action("start")})

    elif text == "/stopscanner":
        log_command(user_id, text, "executed")
        return jsonify({"ok": True, "message": systemctl_action("stop")})

    elif text == "/statusscanner":
        result = subprocess.run(["systemctl", "is-active", "scanner.service"], capture_output=True, text=True)
        log_command(user_id, text, result.stdout.strip())
        return jsonify({"ok": True, "message": f"📡 scanner.service is: {result.stdout.strip()}"})

    elif text == "/startbot":
        try:
            subprocess.run(["sudo", "systemctl", "start", "bot.service"], check=True)
            log_command(user_id, text, "executed")
            return jsonify({"ok": True, "message": "🚀 oanda_webhook_bot.service started"})
        except:
            log_command(user_id, text, "error")
            return jsonify({"ok": False, "message": "❌ Failed to start bot.service"})

    elif text == "/stopbot":
        try:
            subprocess.run(["sudo", "systemctl", "stop", "bot.service"], check=True)
            log_command(user_id, text, "executed")
            return jsonify({"ok": True, "message": "🛑 oanda_webhook_bot.service stopped"})
        except:
            log_command(user_id, text, "error")
            return jsonify({"ok": False, "message": "❌ Failed to stop bot.service"})

    elif text == "/reboot":
        PENDING_ACTIONS[user_id] = "reboot"
        log_command(user_id, text, "pending")
        return jsonify({"ok": True, "message": "⚠️ Are you sure? Reply with `/confirm reboot`"})

    elif text == "/shutdown":
        PENDING_ACTIONS[user_id] = "shutdown"
        log_command(user_id, text, "pending")
        return jsonify({"ok": True, "message": "⚠️ Are you sure? Reply with `/confirm shutdown`"})

    elif text.startswith("/confirm"):
        action = text.replace("/confirm", "").strip()
        if PENDING_ACTIONS.get(user_id) == action:
            log_command(user_id, f"/confirm {action}", "confirmed")
            if action == "reboot":
                subprocess.Popen(["sudo", "reboot"])
                return jsonify({"ok": True, "message": "🔄 Rebooting system..."})
            elif action == "shutdown":
                subprocess.Popen(["sudo", "shutdown", "-h", "now"])
                return jsonify({"ok": True, "message": "🛑 Shutting down EC2..."})
        else:
            log_command(user_id, text, "rejected")
            return jsonify({"ok": False, "message": "❌ No matching pending action or wrong confirmation."})

    elif text == "/logs":
        cursor = db.execute("SELECT ts, user_id, command, status FROM command_logs ORDER BY ts DESC LIMIT 10")
        rows = cursor.fetchall()
        if not rows:
            return jsonify({"ok": True, "message": "No logs found."})

        log_lines = ["📜 *Last 10 Command Logs:*"]
        for ts, uid, cmd, status in rows:
            log_lines.append(f"`{ts}` - {cmd} ({status})")

        return jsonify({"ok": True, "message": "\n".join(log_lines), "parse_mode": "Markdown"})

    elif text == "/help":
        help_msg = (
            "📡 *Available Commands:*\n"
            "/startscanner — Start RSI scanner\n"
            "/stopscanner — Stop RSI scanner\n"
            "/statusscanner — Scanner status\n"
            "/startbot — Start the Flask bot\n"
            "/stopbot — Stop the Flask bot\n"
            "/reboot — Reboot EC2 (requires confirmation)\n"
            "/shutdown — Shut down EC2 (requires confirmation)\n"
            "/confirm reboot — Confirm reboot\n"
            "/confirm shutdown — Confirm shutdown\n"
            "/logs — Show last 10 command logs"
        )
        return jsonify({"ok": True, "message": help_msg, "parse_mode": "Markdown"})

    return jsonify({"ok": False, "message": "Unknown command"})


# === ROUTE: Healthcheck JSON ===
@app.route("/", methods=["GET"])
def healthcheck():
    return jsonify({
        "service": "OANDA Webhook Bot",
        "status": "ok",
        "account_id": ACCOUNT_ID,
        "env": {
            "OANDA_API_TOKEN": "✔️ Loaded" if API_TOKEN else "❌ Missing",
            "WEBHOOK_SECRET": "✔️ Loaded" if WEBHOOK_SECRET else "❌ Missing"
        },
        "trade_logs_count": db.execute("SELECT COUNT(*) FROM trades").fetchone()[0]
    })


# === ROUTE: HTML Dashboard ===
@app.route("/dashboard", methods=["GET"])
def dashboard():
    cursor = db.execute("SELECT ts, user_id, command, status FROM command_logs ORDER BY ts DESC LIMIT 50")
    rows = cursor.fetchall()

    html = "<h2>📊 Telegram Command Logs</h2><table border='1' cellpadding='5'>"
    html += "<tr><th>Time</th><th>User ID</th><th>Command</th><th>Status</th></tr>"

    for ts, uid, cmd, status in rows:
        html += f"<tr><td>{ts}</td><td>{uid}</td><td>{cmd}</td><td>{status}</td></tr>"

    html += "</table>"
    return html


# === Run Flask App ===
if __name__ == "__main__":
    print("🚀 Starting Webhook Bot on port 5001...")
    app.run(host="0.0.0.0", port=5001)
