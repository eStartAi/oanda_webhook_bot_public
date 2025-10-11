# utils/risk.py
# Stub for risk management & position sizing

def calculate_units(balance, risk_percent, stop_loss_pips):
    print(f"[RISK] Balance={balance}, Risk={risk_percent}%, SL={stop_loss_pips} pips")
    return 1000
import os

TRAILING_STOP_ENABLED = os.getenv("TRAILING_STOP_ENABLED", "false").lower() == "true"
TRAILING_STOP_PIPS = float(os.getenv("TRAILING_STOP_PIPS", "10"))

def pip_size_for(instrument: str) -> float:
    if instrument.endswith("_JPY"):
        return 0.01
    return 0.0001

def price_distance_from_pips(instrument: str, pips: float) -> float:
    return pip_size_for(instrument) * pips
