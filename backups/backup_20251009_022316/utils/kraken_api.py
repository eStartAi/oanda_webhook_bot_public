import os
import krakenex
from dotenv import load_dotenv

load_dotenv()

DRY_RUN = os.getenv("DRY_RUN", "1") == "1"

# Your live Kraken API keys
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_API_SECRET = os.getenv("KRAKEN_API_SECRET")

api = krakenex.API()
api.key = KRAKEN_API_KEY
api.secret = KRAKEN_API_SECRET


def place_order(symbol: str, side: str, volume: float, order_type="market", price=None):
    if DRY_RUN:
        print(f"🧪 DRY_RUN - Simulating {side.upper()} {volume} {symbol} @ {price or order_type}")
        return {"status": "dry_run", "side": side, "symbol": symbol, "volume": volume, "price": price}

    order_data = {
        "pair": symbol,
        "type": side,
        "ordertype": order_type,
        "volume": str(volume)
    }

    if order_type == "limit" and price:
        order_data["price"] = str(price)

    response = api.query_private("AddOrder", order_data)
    return response


def get_balance():
    if DRY_RUN:
        return {"ZUSD": "10000.00", "XXBT": "1.23456789"}
    return api.query_private("Balance")


def get_open_orders():
    return api.query_private("OpenOrders")


# Optional: Run test
if __name__ == "__main__":
    print("🔧 Testing Kraken connection... DRY_RUN =", DRY_RUN)
    print(get_balance())
