#!/bin/bash
# manage_backups.sh
# Usage:
#   ./manage_backups.sh save          -> creates next version for main.py & auto_close.py
#   ./manage_backups.sh promote main <num> -> promotes main_V<num>.py to main_backup.py
#   ./manage_backups.sh promote auto <num> -> promotes auto_close_V<num>.py to auto_close_backup.py

# Save mode: create new version snapshots
if [ "$1" == "save" ]; then
  # Main.py
  latest_main=$(ls main_V*.py 2>/dev/null | sed -E 's/.*V([0-9]+)\.py/\1/' | sort -n | tail -1)
  next_main=$((latest_main + 1))
  cp main.py main_V${next_main}.py
  echo "✅ Saved main.py as main_V${next_main}.py"

  # Auto_close.py
  latest_auto=$(ls auto_close_V*.py 2>/dev/null | sed -E 's/.*V([0-9]+)\.py/\1/' | sort -n | tail -1)
  next_auto=$((latest_auto + 1))
  cp auto_close.py auto_close_V${next_auto}.py
  echo "✅ Saved auto_close.py as auto_close_V${next_auto}.py"

# Promote mode: copy version to backup
elif [ "$1" == "promote" ] && [ -n "$2" ] && [ -n "$3" ]; then
  if [ "$2" == "main" ]; then
    version="main_V$3.py"
    if [ -f "$version" ]; then
      cp "$version" main_backup.py
      echo "🔄 Promoted $version → main_backup.py"
    else
      echo "❌ Version $version not found!"
    fi
  elif [ "$2" == "auto" ]; then
    version="auto_close_V$3.py"
    if [ -f "$version" ]; then
      cp "$version" auto_close_backup.py
      echo "🔄 Promoted $version → auto_close_backup.py"
    else
      echo "❌ Version $version not found!"
    fi
  else
    echo "❌ Unknown target: $2 (use 'main' or 'auto')"
  fi

else
  echo "Usage:"
  echo "  $0 save"
  echo "  $0 promote main <num>"
  echo "  $0 promote auto <num>"
fi
