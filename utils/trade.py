# utils/trade.py
# Stub for trade execution logic

def place_order(symbol, side, price, units):
    print(f"[TRADE] {side} {units} {symbol} at {price}")
    return {"status": "stub", "symbol": symbol, "side": side, "price": price}
def close_losing_positions():
    ...
    for pos in positions:
        unrealizedPL = float(pos["unrealizedPL"])
        ...
import os, json, urllib.request
from utils.risk import TRAILING_STOP_ENABLED, TRAILING_STOP_PIPS, price_distance_from_pips

OANDA_API_TOKEN = os.getenv("OANDA_API_TOKEN")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
OANDA_HOST = os.getenv("OANDA_HOST", "https://api-fxpractice.oanda.com")

def _oanda_req(path, payload):
    url = f"{OANDA_HOST}/v3/accounts/{OANDA_ACCOUNT_ID}{path}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {OANDA_API_TOKEN}")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def create_trailing_stop(instrument: str, trade_id: str):
    if not TRAILING_STOP_ENABLED:
        return None
    distance = price_distance_from_pips(instrument, TRAILING_STOP_PIPS)
    payload = {
        "trailingStopLossOrder": {
            "type": "TRAILING_STOP_LOSS",
            "tradeID": trade_id,
            "distance": f"{distance:.10f}",
            "timeInForce": "GTC"
        }
    }
    try:
        return _oanda_req("/orders", payload)
    except Exception as e:
        return {"error": str(e)}
