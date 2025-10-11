import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'scanner.log')

def log_message(message: str):
    """Write a timestamped log message to scanner.log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    print(formatted)
    with open(LOG_FILE, "a") as f:
        f.write(formatted + "\n")
# utils/logger.py
# Stub for trade logging

def log_trade(symbol, side, price, result="pending"):
    print(f"[LOGGER] {side} {symbol} at {price} result={result}")
