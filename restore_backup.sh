#!/bin/bash
# Restore last backup of your bot

BOT_DIR="oanda_webhook_bot"
BACKUP_DIR=$(ls -td oanda_webhook_bot_backup_* | head -1)

if [ -z "$BACKUP_DIR" ]; then
  echo "❌ No backup folder found!"
  exit 1
fi

echo "🔄 Restoring from backup: $BACKUP_DIR"
rm -rf "$BOT_DIR"
cp -r "$BACKUP_DIR" "$BOT_DIR"

echo "✅ Restore complete! Your bot has been rolled back to: $BACKUP_DIR"
