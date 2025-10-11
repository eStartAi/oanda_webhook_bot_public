#!/bin/bash
set -e

MODE=$1
if [ -z "$MODE" ]; then
  echo "Usage: $0 [sandbox|live|status]"
  exit 1
fi

APP_PORT=$(grep APP_PORT .env | cut -d '=' -f2)

print_status() {
  DASH=$(curl -s http://localhost:$APP_PORT/dashboard || true)
  if [ -n "$DASH" ]; then
    if command -v jq >/dev/null 2>&1; then
      RUN_MODE=$(echo $DASH | jq -r '.status.run_mode')
      EXCHANGE=$(echo $DASH | jq -r '.status.exchange')
      DRY_RUN=$(echo $DASH | jq -r '.status.dry_run')
      BALANCE=$(echo $DASH | jq -r '.status.balance')
      echo "✅ ScaleViper is UP on port $APP_PORT"
      echo "   • Run Mode : $RUN_MODE"
      echo "   • Exchange : $EXCHANGE"
      echo "   • Dry Run  : $DRY_RUN"
      echo "   • Balance  : $BALANCE"
    else
      echo "✅ ScaleViper is UP on port $APP_PORT"
      echo "⚠️ Install jq for detailed status: sudo apt-get install -y jq"
    fi
    return 0
  else
    echo "❌ ScaleViper is NOT responding — showing last 10 log lines:"
    tail -n 10 logs/scaleviper.log
    return 1
  fi
}

if [ "$MODE" == "status" ]; then
  echo "🔎 Checking ScaleViper status on port $APP_PORT..."
  print_status
  exit $?
fi

echo "🔁 Restarting ScaleViper..."
echo "🔧 Using $MODE environment"

# Kill any OANDA bot or old ScaleViper Python process
echo "🛑 Stopping any existing bots..."
pkill -f oanda_webhook_bot/venv/bin/python3 || true
pkill -f scaleviper/main.py || true

# Backup step (optional, safe fallback)
if [ -f manage_backups.sh ]; then
  echo "📦 Creating backup before restart..."
  ./manage_backups.sh save || true
fi

# Switch .env file to mode
if [ "$MODE" == "sandbox" ]; then
  sed -i 's/^RUN_MODE=.*/RUN_MODE=sandbox/' .env
  sed -i 's/^DRY_RUN=.*/DRY_RUN=true/' .env
elif [ "$MODE" == "live" ]; then
  echo "⚠️ WARNING: You are about to start ScaleViper in LIVE mode!"
  echo "This will place REAL trades on exchange: $(grep DEFAULT_BROKER .env | cut -d '=' -f2)"
  read -p "Are you sure? (yes/NO): " CONFIRM
  if [[ "$CONFIRM" != "yes" ]]; then
    echo "❌ Live mode aborted."
    exit 1
  fi
  sed -i 's/^RUN_MODE=.*/RUN_MODE=webhook/' .env
  sed -i 's/^DRY_RUN=.*/DRY_RUN=false/' .env
fi

echo "🚀 Starting ScaleViper on port $APP_PORT..."
source venv/bin/activate
nohup python3 main.py > logs/scaleviper.log 2>&1 &

sleep 3
echo "🔎 Checking bot status..."
if print_status; then
  echo "✅ Bot restart sequence completed ($MODE mode, port $APP_PORT)"
else
  echo "❌ Restart failed — check logs above."
fi
