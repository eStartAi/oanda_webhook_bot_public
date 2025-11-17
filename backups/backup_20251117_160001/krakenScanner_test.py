import time
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from utils.logger import log_message  # use your existing logger

# === CONFIG ===
WATCHLIST = ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD"]
INTERVAL = 1  # minutes per candle
LOOP_DELAY = 60  # seconds
LOOKBACK = 100
TEST_MODE = True  # ensures no live webhooks
PRINT_THRESHOLD = 0.0  # only print if confidence >= threshold

def fetch_ohlc(pair, interval=1):
    """Fetch OHLCV data from Kraken public API."""
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair.replace('/', '')}&interval={interval}"
    try:
        r = requests.get(url)
        data = r.json()
        key = list(data['result'].keys())[0]
        df = pd.DataFrame(data['result'][key], columns=[
            'time','open','high','low','close','vwap','volume','count'
        ])
        df = df.astype(float)
        df['close'] = df['close'].astype(float)
        return df
    except Exception as e:
        log_message(f"❌ Error fetching {pair}: {e}")
        return None

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

# === SIGNAL SCORE ===
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

# === MAIN LOOP ===
def run_scanner():
    print("🔍 Starting Kraken Scanner (TEST MODE)")
    while True:
        for pair in WATCHLIST:
            df = fetch_ohlc(pair, INTERVAL)
            if df is None or len(df) < LOOKBACK:
                continue

            df['rsi'] = calc_rsi(df['close'])
            df['macd'], df['macd_signal'] = calc_macd(df['close'])
            df['ema_slope'] = calc_ema_slope(df['close'])
            df['atr'] = calc_atr(df)
            df['vol_spike'] = calc_volume_spike(df['volume'])

            score = score_signal(df)
            last_close = df['close'].iloc[-1]
            signal_type = "BUY" if df['macd'].iloc[-1] > df['macd_signal'].iloc[-1] else "SELL"

            if score >= PRINT_THRESHOLD:
                msg = f"[{datetime.now().strftime('%H:%M:%S')}] {pair} {signal_type} | Score: {score}/10 | Price: {last_close:.2f}"
                print(msg)
                log_message(msg)
        time.sleep(LOOP_DELAY)

if __name__ == "__main__":
    run_scanner()
