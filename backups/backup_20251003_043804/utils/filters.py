import os, time, json, urllib.request
from collections import defaultdict
from math import fabs

OANDA_API_TOKEN = os.getenv("OANDA_API_TOKEN")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
OANDA_HOST = os.getenv("OANDA_HOST", "https://api-fxpractice.oanda.com")

AI_ENABLED = os.getenv("AI_FILTER_ENABLED", "false").lower() == "true"
AI_MIN_COOLDOWN_SEC = int(os.getenv("AI_MIN_COOLDOWN_SEC", "120"))
AI_ATR_PERIOD = int(os.getenv("AI_ATR_PERIOD", "14"))
AI_ATR_MIN = float(os.getenv("AI_ATR_MIN", "0.0008"))
AI_ATR_MAX = float(os.getenv("AI_ATR_MAX", "0.0080"))

_last_trade_ts = defaultdict(lambda: 0.0)

def _oanda_get(path, params: dict):
    url = f"{OANDA_HOST}/v3/{path}"
    if params:
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{qs}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {OANDA_API_TOKEN}")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def _atr(candles):
    trs = []
    prev_close = None
    for c in candles:
        h = float(c["mid"]["h"])
        l = float(c["mid"]["l"])
        close = float(c["mid"]["c"])
        if prev_close is None:
            tr = h - l
        else:
            tr = max(h - l, fabs(h - prev_close), fabs(l - prev_close))
        trs.append(tr)
        prev_close = close
    return sum(trs[-AI_ATR_PERIOD:]) / min(AI_ATR_PERIOD, len(trs))

def ai_gate_allow(instrument: str, granularity="M5") -> (bool, str):
    if not AI_ENABLED:
        return (True, "AI filter disabled")

    now = time.time()
    if now - _last_trade_ts[instrument] < AI_MIN_COOLDOWN_SEC:
        return (False, f"Cooldown active {AI_MIN_COOLDOWN_SEC}s for {instrument}")

    try:
        r = _oanda_get(f"instruments/{instrument}/candles", {
            "count": max(20, AI_ATR_PERIOD+1),
            "price": "M",
            "granularity": granularity
        })
        candles = [c for c in r.get("candles", []) if c.get("complete")]
        if len(candles) < AI_ATR_PERIOD:
            return (False, "Not enough candles")
        atr = _atr(candles)
    except Exception as e:
        return (False, f"ATR fetch failed: {e}")

    if atr < AI_ATR_MIN:
        return (False, f"ATR too low: {atr:.6f}")
    if atr > AI_ATR_MAX:
        return (False, f"ATR too high: {atr:.6f}")

    return (True, f"Allowed (ATR={atr:.6f})")

def record_trade(instrument: str):
    _last_trade_ts[instrument] = time.time()
