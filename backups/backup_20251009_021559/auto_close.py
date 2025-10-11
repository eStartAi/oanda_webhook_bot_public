from dotenv import load_dotenv
load_dotenv()

from utils.notify import telegram_notify

# Replace with your actual logic

def run_auto_close():
    return [
        {"instrument": "EUR_USD", "units": -1000, "pl": -2.45},
        {"instrument": "GBP_USD", "units": -1000, "pl": -3.12}
    ]


    """
    Your logic here to close all losing positions.
    Return a list of closed trades like:
    [
        {
            'instrument': 'EUR_USD',
            'units': -1000,
            'pl': -4.56,
            'reason': 'daily_auto_close'
        },
        ...
    ]
    """
    # Example stub data
    return [
        {"instrument": "EUR_USD", "units": -1000, "pl": -4.32},
        {"instrument": "GBP_USD", "units": -1000, "pl": -1.89},
    ]


def _format_money(v):
    return f"${v:,.2f}"


def notify_auto_close(closed):
    if not closed:
        telegram_notify("🧹 Auto-close ran — no open losing positions found.")
        return

    lines = ["🧹 Auto-close summary:"]
    total_pl = 0.0
    for c in closed:
        total_pl += float(c.get("pl", 0) or 0)
        lines.append(f"• {c['instrument']}: units {c['units']}, P/L {_format_money(float(c['pl']))}")
    lines.append(f"\nTotal P/L: {_format_money(total_pl)}")
    telegram_notify("\n".join(lines))


if __name__ == "__main__":
    closed = run_auto_close()
    notify_auto_close(closed)
import os

# ✅ Trigger Telegram DM after auto-close (if enabled)
if os.getenv("ENABLE_TELEGRAM_ALERTS", "false").lower() == "true":
    os.environ["TELEGRAM_MESSAGE"] = "📉 Auto-close completed for all open positions (21:00 UTC)"
    os.system("python3 notify.py")

