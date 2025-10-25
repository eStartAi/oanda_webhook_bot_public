import logging

def validate_risk(symbol, side, price, size):
    """
    Basic placeholder risk check.
    Returns True if trade size > 0 and price > 0.
    Later you can add checks for:
    - Daily profit target reached
    - Max daily loss
    - Max consecutive losses
    - Spread filters, etc.
    """
    if size <= 0 or price <= 0:
        logging.warning(f"Risk check failed: size={size}, price={price}")
        return False

    # ✅ Always true for now (basic validation only)
    return True
