#!/bin/bash

# === Usage ===
# ./manage_backups.sh save
# ./manage_backups.sh promote main 3
# ./manage_backups.sh promote auto 2

if [ "$1" = "save" ]; then
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_dir="backups"
    mkdir -p "$backup_dir"

    path="$backup_dir/backup_$timestamp"
    echo "🔒 Saving backup to $path"
    
    # Save full folder snapshot (excluding unwanted dirs)
    rsync -a --exclude 'backups' --exclude '.git' ./ "$path"

    echo "✅ Backup complete: $path"

    # Detect environment: Kraken (live) or OANDA (practice)
    if grep -q "KRAKEN_API_KEY" .env; then
        mode="live"
    else
        mode="practice"
    fi

    # Auto-update checklist
    ./manage_checklist.sh "$mode" "$path"

    echo -e "\n🟢 Do you want to commit & push this backup to GitHub? (yes/no)"
    read -r answer
    if [[ "$answer" == "yes" || "$answer" == "y" ]]; then
        git add "$path" CHECKLIST.md
        git commit -m "🔒 Backup + checklist update: $timestamp"
        ./git_safe_sync.sh
    else
        echo "🚫 Git push skipped."
    fi

elif [ "$1" = "promote" ]; then
    if [ "$#" -ne 3 ]; then
        echo "Usage: $0 promote [main|auto] <N>"
        exit 1
    fi

    slot="$2"
    number="$3"
    src=$(ls -dt backups/backup_* | sed -n "${number}p")
    dst="$backup_dir/$slot"

    echo "📤 Promoting $src → $dst"
    rm -rf "$dst"
    cp -r "$src" "$dst"
    echo "✅ Promoted to $dst"

else
    echo "Usage:"
    echo "  $0 save"
    echo "  $0 promote [main|auto] <N>"
fi
