def calculate_signal_score(data):
    """
    Very simple scoring function for demo.
    Replace with real RSI, MACD, EMA logic later.
    """
    score = 0
    if data.get("rsi", 50) < 30:
        score += 3
    if data.get("macd_cross", False):
        score += 2
    if data.get("ema50", 0) > data.get("ema200", 0):
        score += 2
    if data.get("volume", 0) > data.get("volume_ma", 0):
        score += 1
    if data.get("candle_pattern") == "bullish_engulfing":
        score += 2
    return min(score, 10)
