import asyncio
import aiohttp
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from utils.logger import log_message
from dotenv import load_dotenv
import requests

load_dotenv()

# === CONFIG ===
WATCHLIST = [
    "BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD", "DOGE/USD",
    "LTC/USD", "ADA/USD", "MATIC/USD", "AVAX/USD",
    "DOT/USD", "LINK/USD", "BNB/USD"
]

# Kraken's internal pair codes differ for some assets
PAIR_MAP = {
    "BTC/USD": "XXBTZUSD",
    "ETH/USD": "XETHZUSD",
    "SOL/USD": "SOLUSD",
    "XRP/USD": "XXRPZUSD",
    "DOGE/USD": "DOGEUSD",
    "LTC/USD": "XLTCZUSD",
    "ADA/USD": "ADAUSD",
    "MATIC/USD": "MATICUSD",
    "AVAX/USD": "AVAXUSD",
    "DOT/USD": "DOTUSD",
    "LINK/USD": "LINKUSD",
    "BNB/USD": "BNBUSD",
}

INTERVAL = 1
LOOKBACK = 100
LOOP_DELAY = 60
COOLDOWN_MINUTES = 5
PRINT_THRESHOLD = 0.0

SCALEVIPER_WEBHOOK = os.getenv("SCALEVIPER_WEBHOOK_URL", "http://127.0.0.1:5003/webhook")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret")

last_sent = {}

# === INDICATORS ===
def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calc_macd(series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def calc_ema_slope(series, period=20):
    ema = series.ewm(span=period, adjust=False).mean()
    slope = np.degrees(np.arctan((ema.diff() / ema.shift()).fillna(0)))
    return slope

def calc_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def calc_volume_spike(volume, period=20):
    avg_vol = volume.rolling(period).mean()
    return volume / avg_vol

def score_signal(df):
    rsi = df['rsi'].iloc[-1]
    macd, signal = df['macd'].iloc[-1], df['macd_signal'].iloc[-1]
    ema_slope = df['ema_slope'].iloc[-1]
    atr = df['atr'].iloc[-1]
    vol_spike = df['vol_spike'].iloc[-1]

    score = 0
    if rsi < 30: score += 2
    elif rsi > 70: score += 2
    if macd > signal: score += 2
    if ema_slope > 0: score += 2
    if vol_spike > 1.5: score += 2
    if atr > df['atr'].mean(): score += 2

    return round(min(score, 10), 2)

# === ASYNC FETCH ===
async def fetch_ohlc(session, pair, interval):
    kraken_pair = PAIR_MAP.get(pair, pair.replace("/", ""))
    url = f"https://api.kraken.com/0/public/OHLC?pair={kraken_pair}&interval={interval}"
    try:
        async with session.get(url, timeout=10) as resp:
            data = await resp.json()
            key = list(data["result"].keys())[0]
            df = pd.DataFrame(data["result"][key], columns=[
                "time", "open", "high", "low", "close", "vwap", "volume", "count"
            ])
            df = df.astype(float)
            return pair, df
    except Exception as e:
        log_message(f"❌ Error fetching {pair}: {e}")
        return pair, None

def send_to_scaleviper(pair, side, score, price):
    now = datetime.utcnow()
    if pair in last_sent and (now - last_sent[pair]) < timedelta(minutes=COOLDOWN_MINUTES):
        log_message(f"⏸️ Cooldown active for {pair}, skipping...")
        return

    payload = {
        "secret": WEBHOOK_SECRET,
        "pair": pair,
        "side": side,
        "price": price,
        "score": score,
        "timestamp": now.isoformat()
    }
    try:
        r = requests.post(SCALEVIPER_WEBHOOK, json=payload, timeout=5)
        if r.status_code == 200:
            log_message(f"✅ Sent {pair} {side} ({score}/10) @ {price:.2f}")
            last_sent[pair] = now
        else:
            log_message(f"⚠️ Webhook failed [{r.status_code}]: {r.text}")
    except Exception as e:
        log_message(f"❌ Webhook error: {e}")

# === MAIN LOOP ===
async def run_scanner():
    print("⚡ Kraken Scanner (Async + Pair Map + Cooldown) running...")
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [fetch_ohlc(session, pair, INTERVAL) for pair in WATCHLIST]
            results = await asyncio.gather(*tasks)

            for pair, df in results:
                if df is None or len(df) < LOOKBACK:
                    continue

                df["rsi"] = calc_rsi(df["close"])
                df["macd"], df["macd_signal"] = calc_macd(df["close"])
                df["ema_slope"] = calc_ema_slope(df["close"])
                df["atr"] = calc_atr(df)
                df["vol_spike"] = calc_volume_spike(df["volume"])

                score = score_signal(df)
                last_close = df["close"].iloc[-1]
                side = "BUY" if df["macd"].iloc[-1] > df["macd_signal"].iloc[-1] else "SELL"

                msg = f"[{datetime.now().strftime('%H:%M:%S')}] {pair} {side} | Score: {score}/10 | Price: {last_close:.2f}"
                print(msg)
                log_message(msg)

                if score >= PRINT_THRESHOLD:
                    send_to_scaleviper(pair, side, score, last_close)

            await asyncio.sleep(LOOP_DELAY)

if __name__ == "__main__":
    asyncio.run(run_scanner())
