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
