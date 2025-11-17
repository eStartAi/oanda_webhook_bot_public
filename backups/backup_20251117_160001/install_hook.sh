#!/bin/bash

HOOK_PATH=".git/hooks/pre-push"

echo "🛠 Installing pre-push hook to protect public repo..."

# Create .git/hooks directory if missing
mkdir -p .git/hooks

# Write the pre-push hook
cat > "$HOOK_PATH" << 'EOF'
#!/bin/bash

# === SENSITIVE FILE PATTERNS TO BLOCK ===
BLOCKED_PATTERNS=(
  ".env"
  "*.db"
  "*.log"
  "nohup.out"
)

REMOTE_NAME="$1"

# Only trigger this for the public mirror remote
if [[ "$REMOTE_NAME" == "public" ]]; then
  echo "🔒 Scanning for sensitive files in push to 'public'..."

  FILES=$(git diff --cached --name-only)

  for pattern in "${BLOCKED_PATTERNS[@]}"; do
    for file in $FILES; do
      if [[ "$file" == $pattern || "$file" == *"${pattern#*.}" ]]; then
        echo "❌ ERROR: Attempt to push sensitive file '$file' to public repo."
        echo "🛑 Push blocked. Please clean or exclude these files."
        exit 1
      fi
    done
  done

  echo "✅ No sensitive files detected. Safe to push."
fi

exit 0
EOF

# Make it executable
chmod +x "$HOOK_PATH"

echo "✅ pre-push hook installed at $HOOK_PATH"

