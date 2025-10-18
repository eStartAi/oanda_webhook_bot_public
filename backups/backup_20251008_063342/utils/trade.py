import logging

def execute_trade(exchange, symbol, side, order_type="market", price=0, size=0):
    """
    Route order to the correct exchange.
    Extend this with broker-specific API modules.
    """
    if exchange == "kraken":
        return _execute_kraken(symbol, side, order_type, price, size)

    raise ValueError(f"Exchange {exchange} not supported yet.")


def _execute_kraken(symbol, side, order_type, price, size):
    """
    Kraken API execution (stub).
    Replace with actual kraken-python-api calls.
    """
    logging.info(f"🐙 Kraken {side.upper()} {symbol} {order_type} {size} @ {price}")
    # TODO: integrate with `krakenex` or REST API
    return {
        "exchange": "kraken",
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "price": price,
        "size": size,
        "status": "success_stub"
    }
