#!/bin/bash

# === CONFIGURATION ===
PRIVATE_REPO_SSH="git@github.com:eStartAi/oanda_webhook_bot.git"
PUBLIC_REPO_SSH="git@github.com:eStartAi/oanda_webhook_bot_public.git"
BRANCH="main"

# === START ===
echo "📁 Navigating to project folder..."
cd "$(dirname "$0")" || exit 1

# Initialize if not a git repo
if [ ! -d .git ]; then
  echo "🔧 Initializing Git repository..."
  git init
fi

# Confirm current branch is correct
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null)
if [[ "$CURRENT_BRANCH" != "$BRANCH" ]]; then
  echo "🔀 Creating or switching to branch: $BRANCH"
  git checkout -B "$BRANCH"
fi

echo "📦 Adding all files..."
git add -A

# Prompt for commit message
read -rp "💬 Enter commit message: " COMMIT_MSG
COMMIT_MSG=${COMMIT_MSG:-"Auto commit: Push all contents"}

echo "✅ Committing..."
git commit -m "$COMMIT_MSG" || echo "⚠️ Nothing to commit"

# Set remote for private repo
git remote remove origin 2>/dev/null
echo "🔗 Adding private repo remote..."
git remote add origin "$PRIVATE_REPO_SSH"

# Push to private repo
echo "🚀 Pushing to private GitHub repo..."
git push -u origin "$BRANCH"

# Ask for public mirror push
read -rp "🌍 Do you also want to push to public mirror repo? (y/n): " PUSH_PUBLIC

if [[ $PUSH_PUBLIC == "y" || $PUSH_PUBLIC == "Y" ]]; then
  echo "🔗 Adding public mirror remote..."
  git remote remove public 2>/dev/null
  git remote add public "$PUBLIC_REPO_SSH"

  echo "🚀 Pushing to public mirror repo (force sync)..."
  git push --force public "$BRANCH"
fi

echo "✅ Done."
