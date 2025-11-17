#!/bin/bash

LOGFILE="logs/sync_dashboard.log"
mkdir -p logs

{
echo "🔄 [$(date)] Starting git_safe_sync.sh..."

cd ~/scaleviper || { echo "❌ Cannot cd into scaleviper"; exit 1; }

git add .
COMMIT_MSG="🔄 Auto-sync $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG" --allow-empty

echo "📥 Rebasing with origin..."
if ! git pull origin main --rebase; then
  echo "❌ Rebase failed"
  TELEGRAM_MESSAGE="⚠️ Git Safe Sync FAILED (rebase)" python3 notify.py 2>> logs/telegram_errors.log
  exit 1
fi

echo "📤 Pushing to origin..."
git push origin main || {
  echo "❌ Origin push failed"
  TELEGRAM_MESSAGE="⚠️ Git Safe Sync FAILED (origin push)" python3 notify.py 2>> logs/telegram_errors.log
  exit 2
}

echo "🌍 Force pushing to public..."
git push public main --force || {
  echo "❌ Public push failed"
  TELEGRAM_MESSAGE="⚠️ Git Safe Sync FAILED (public push)" python3 notify.py 2>> logs/telegram_errors.log
  exit 3
}

TELEGRAM_MESSAGE="✅ Git Safe Sync SUCCESS at $(date)" python3 notify.py 2>> logs/telegram_errors.log
echo "✅ git_safe_sync.sh completed successfully"

} >> "$LOGFILE" 2>&1


TELEGRAM_MESSAGE="✅ Git Safe Sync SUCCESS at $(date)" python3 notify.py 2>> logs/telegram_errors.log
SUMMARY="📊 Summary: Git sync ✅ | Telegram ✅"
echo "$SUMMARY"
