def load_state():
    return {"current_balance": 1000, "trades": []}

def reset_daily_stats_if_needed(state):
    return state

def update_after_trade(state, pnl_pct, trade_won):
    state["current_balance"] *= (1 + pnl_pct/100)
    return state

def check_trading_allowed(state):
    return True, "Trading allowed"
