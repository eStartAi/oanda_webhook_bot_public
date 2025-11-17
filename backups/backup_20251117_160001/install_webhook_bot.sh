
#!/bin/bash

# Set working directory
cd ~/oanda_webhook_bot || exit 1

echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "⬇️ Installing required packages..."
pip install --upgrade pip
pip install flask python-dotenv

echo "🔍 Backing up old main.py (if exists)..."
[ -f main.py ] && mv main.py main_backup_$(date +%s).py

echo "📦 Using new webhook bot with TP/SL/auto size..."
mv main_with_sizing.py main.py

echo "🚀 Starting Webhook Bot on port 5001..."
python3 main.py
