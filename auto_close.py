import os
import sqlite3
from dotenv import load_dotenv
import oandapyV20
import oandapyV20.endpoints.trades as trades

# Load env
load_dotenv()
API_KEY = os.getenv("OANDA_API_TOKEN")
ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")

if not API_KEY or not ACCOUNT_ID:
    raise EnvironmentError("Missing OANDA_API_TOKEN or OANDA_ACCOUNT_ID in .env")

# DB
DB_FILE = "trade_logs.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cur = conn.cursor()

# OANDA client
client = oandapyV20.API(access_token=API_KEY)

def close_all_trades():
    print("🔒 Closing all open trades...")
    try:
        r = trades.OpenTrades(ACCOUNT_ID)
        client.request(r)
        open_trades = r.response.get("trades", [])

        if not open_trades:
            print("✅ No open trades found.")
            return

        for t in open_trades:
            trade_id = t["id"]
            instrument = t["instrument"]
            units = t["currentUnits"]

            print(f"➡️ Closing {instrument} trade {trade_id} ({units} units)")
            try:
                close_req = trades.TradeClose(ACCOUNT_ID, tradeID=trade_id, data={"units": "ALL"})
                client.request(close_req)
                cur.execute("INSERT INTO trades (symbol, side, price, units, sl, tp, trail, status) VALUES (?,?,?,?,?,?,?,?)",
                            (instrument, "AUTO-CLOSE", 0, int(units), 0, 0, 0, "CLOSED"))
                conn.commit()
                print(f"✅ Closed trade {trade_id}")
            except Exception as e:
                print(f"❌ Error closing trade {trade_id}: {e}")

    except Exception as e:
        print("❌ Error fetching open trades:", e)

if __name__ == "__main__":
    close_all_trades()
