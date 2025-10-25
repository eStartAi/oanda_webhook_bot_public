import json
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)
LOG_FILE = "logs/trades.jsonl"
ERROR_FILE = "logs/errors.log"

def log_trade(trade_data):
    if not isinstance(trade_data, dict):
        raise ValueError("log_trade expects a dict")

    print(f"📝 Trade logged: {trade_data.get('pair')} {trade_data.get('side')} @ {trade_data.get('price')} (size={trade_data.get('size')})")

    trade_data["timestamp"] = datetime.utcnow().isoformat()
    open(LOG_FILE, "a").write(json.dumps(trade_data) + "\n")

def log_error(msg):
    print(f"❌ Error logged: {msg}")
    open(ERROR_FILE, "a").write(f"{datetime.utcnow().isoformat()} ERROR: {msg}\n")

def read_trades(limit=None):
    """Read trade history from the JSONL log.
    :param limit: If set, return only the last N trades.
    :return: List of trade dicts.
    """
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        trades = [json.loads(line) for line in f if line.strip()]

    if limit:
        return trades[-limit:]
    return trades

def read_errors(limit=None):
    """Read error history from the error log.
    :param limit: If set, return only the last N errors.
    :return: List of error log lines (strings).
    """
    if not os.path.exists(ERROR_FILE):
        return []

    with open(ERROR_FILE, "r") as f:
        errors = [line.strip() for line in f if line.strip()]

    if limit:
        return errors[-limit:]
    return errors
