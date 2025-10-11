[![Mirror Status](https://github.com/eStartAi/scaleviper/actions/workflows/mirror.yml/badge.svg)](https://github.com/eStartAi/scaleviper/actions/workflows/mirror.yml)
scaleViper
==========

# ⚡️ ScaleViper — Automated Multi-Broker Trading Bot

[![Mirror Status](https://github.com/eStartAi/scaleviper/actions/workflows/mirror.yml/badge.svg)](https://github.com/eStartAi/scaleviper/actions/workflows/mirror.yml)
[![Checklist Reset](https://github.com/eStartAi/scaleviper/actions/workflows/reset_checklist.yml/badge.svg)](https://github.com/eStartAi/scaleviper/actions/workflows/reset_checklist.yml)

> 🚀 **ScaleViper** is a high-frequency, risk-managed scalping bot built for **Forex, Crypto, and Stocks** — integrated with **OANDA**, **Kraken**, and more.

---

### 🔧 Core Features
- 🧠 **AI-Scored Signals** — RSI, MACD, EMA-slope, ATR, and Volume Spike logic  
- 💸 **Auto Position Sizing** — risk-based calculation tied to account balance  
- 🛑 **Risk Guards** — daily profit/loss limits and duplicate-trade blockers  
- 📊 **PnL Logging** — auto-record trades to JSON/SQLite  
- 📤 **Telegram Alerts** — confirmations, kill-switch, and summaries  
- ☁️ **CI/CD Automation** — GitHub → EC2 → Kraken/OANDA live deployment  

---

### 🔁 Repository Sync
- **Private Repo:** [`eStartAi/scaleviper`](https://github.com/eStartAi/scaleviper)  
- **Public Mirror:** [`eStartAi/oanda_webhook_bot_public`](https://github.com/eStartAi/oanda_webhook_bot_public)  
- **Last Synced:** <!--SYNC_DATE-->`2025-10-08 21:00 UTC`<!--/SYNC_DATE-->

The public mirror auto-updates every time you push to `main`.

---

### 📘 Quick Start (Local or EC2)

```bash
# Clone private repo
git clone https://github.com/eStartAi/scaleviper.git
cd scaleviper

# Create and activate venv
python3 -m venv venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in sandbox / live mode
python3 main.py


=====================================================
🛠 Maintained by eStartAi / ScaleViper Team
© 2025 — All rights reserved.
=====================================================



# OANDA Webhook Bot

## Features
- Flask webhook server
- SQLite trade logging
- Modular utils (trade, risk, logger)
- Ready for Render deployment

## Usage
```bash
git clone <repo>
cd oanda_webhook_bot
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Deployment
- Use `render.yaml` for Render deployment.
# oanda_webhook_bot_Private


# OANDA Webhook Bot with Backup Management

## 📦 Features
- Flask webhook bot to trade via OANDA API.
- Auto TP/SL, trailing stops, trade logging.
- Daily auto-close script.
- Backup/versioning system for safe edits.

## 🛠️ Backup Management
We use `manage_backups.sh` to keep versioned copies of `main.py` and `auto_close.py`.

### Save a new snapshot
```bash
./manage_backups.sh save


➡️ Creates main_V#.py and auto_close_V#.py.
Promote a version as the official backup
./manage_backups.sh promote main 2
./manage_backups.sh promote auto 1


➡️ Copies main_V2.py → main_backup.py
➡️ Copies auto_close_V1.py → auto_close_backup.py
Restore from backup
If needed, restore from the latest backup files:
./restore_file_backup.sh

🚀 Deployment
Works on EC2, Render, or any server with Python 3.11+.


Requires .env with:


OANDA_API_TOKEN=your_token_here
OANDA_ACCOUNT_ID=your_account_id_here
WEBHOOK_SECRET=your_webhook_secret
DEFAULT_BROKER=oanda_practice

✅ This way, you’ll never lose a working bot — you can save, promote, and restore versions at will



Perfect 👍 — here’s the automatic append command you can paste directly into your EC2 terminal. It will safely add the snapshot-ignore rules to the end of your existing .gitignore file inside your bot’s folder:


cd ~/oanda_webhook_bot

cat >> .gitignore <<EOL

# Ignore local versioned snapshots
main_V*.py
auto_close_V*.py

# Keep backups tracked
!main_backup.py
!auto_close_backup.py

# Standard ignores
.env
venv/
__pycache__/
*.db
*.log
EOL


🔹 What happens when you run it:
Moves into your oanda_webhook_bot folder.


Appends the ignore rules to .gitignore (doesn’t overwrite anything).


From now on, Git will ignore your local *_V*.py snapshots but will still track your active files and official backups.



👉 After running it, confirm with: cat .gitignore



📌 To install the Git hook:
bash install_hook.sh


📦 Features Recap

✅ Auto detects and switches to main branch

✅ Adds all files (git add -A)

✅ Prompts for custom commit message

✅ Pushes to your private repo:
git@github.com:eStartAi/oanda_webhook_bot.git

✅ Optionally mirrors to your public repo:
git@github.com:eStartAi/oanda_webhook_bot_public.git


🧪 Instructions to Use:
	Save this script as push_all.sh inside your project folder.

	Make it executable & Run
 
		chmod +x push_all.sh
		./push_all.sh


📦 What It Removes from Public Repo.........

File/Pattern			Reason
.env				API keys, secrets
trade_logs.db			Internal trading records
webhook.log			Bot logs
nohup.out			Background process logs
.env.example			Kept (or recreated if missing)


🧪 Usage Instructions

Save as: sync_from_private.sh

Make executable:

chmod +x sync_from_private.sh


Run it:

./sync_from_private.sh


✅ .git/hooks/pre-push

💡 What it Does

Only checks when pushing to public remote

Blocks .env, *.db, *.log, nohup.out

Shows error and aborts the push

Silent/pass-through for other remotes (like origin)💡 What it Does

Only checks when pushing to public remote

Blocks .env, *.db, *.log, nohup.out

Shows error and aborts the push

Silent/pass-through for other remotes (like origin)



🛠 How to Install
Save the hook

bash
Copy code
nano .git/hooks/pre-push
Paste the script above.

Make it executable

bash
Copy code
chmod +x .git/hooks/pre-push


✅ Script: install_hook.sh

🧪 To Use:

Save this as: install_hook.sh

Run:

chmod +x install_hook.sh
./install_hook.sh







echo "🚀 ScaleViper ready for Kraken scalping." >> README.md
git add README.md
git commit -m "🧪 Test mirror sync"
git push

---
Last Synced: 2025-10-11 10:00 UTC
