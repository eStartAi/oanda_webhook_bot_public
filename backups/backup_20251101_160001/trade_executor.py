def place_trade(pair, side, price, size, confidence_score=0):
    print(f"🚀 Executing {side.upper()} {pair} @ {price} (size={size}, score={confidence_score})")
    return {"status": "success", "data": {"pair": pair, "side": side, "price": price, "size": size}}
