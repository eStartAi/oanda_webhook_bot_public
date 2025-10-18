#!/bin/bash

# === CONFIGURATION ===
PRIVATE_REPO_SSH="git@github.com:eStartAi/oanda_webhook_bot.git"
PUBLIC_REPO_SSH="git@github.com:eStartAi/oanda_webhook_bot_public.git"
BRANCH="main"

echo "📁 Navigating to project folder..."
cd "$(dirname "$0")" || exit 1

# Ensure it's a git repo
if [ ! -d .git ]; then
  echo "❌ This is not a git repository. Exiting."
  exit 1
fi

# Ensure we're on correct branch
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null)
if [[ "$CURRENT_BRANCH" != "$BRANCH" ]]; then
  echo "🔀 Switching to $BRANCH branch..."
  git checkout -B "$BRANCH"
fi

# Remove existing remotes just in case
git remote remove origin 2>/dev/null
git remote remove public 2>/dev/null

# Add remotes
git remote add origin "$PRIVATE_REPO_SSH"
git remote add public "$PUBLIC_REPO_SSH"

# Pull from private repo
echo "⬇️  Pulling latest from private repo..."
git pull origin "$BRANCH" || {
  echo "❌ Pull failed. Check SSH/auth access."
  exit 1
}

# Sanitize sensitive files before mirroring
echo "🧹 Cleaning sensitive files..."
rm -f .env trade_logs.db webhook.log nohup.out

# Optionally add a fresh .env.example if needed
if [ -f ".env.example" ]; then
  echo "ℹ️  Keeping .env.example template"
else
  echo "OANDA_API_TOKEN=\nWEBHOOK_SECRET=\nOANDA_ACCOUNT_ID=" > .env.example
  git add .env.example
fi

# Stage changes
git add -A
git commit -m "🚫 Strip sensitive files before public mirror" || echo "⚠️ Nothing to commit"

# Push to public mirror
echo "🚀 Pushing to public repo (force)..."
git push --force public "$BRANCH"

echo "✅ Public mirror sync complete (with cleaned files)."
