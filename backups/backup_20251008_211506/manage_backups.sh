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
    
    # Save full folder snapshot (optional: add more exclusions if needed)
    rsync -a --exclude 'backups' --exclude '.git' ./ "$path"

    echo "✅ Backup complete: $path"

    # Auto-update checklist (default = live, fallback to practice if env shows OANDA)
    if grep -q "KRAKEN_API_KEY" .env; then
        mode="live"
    else
        mode="practice"
    fi

    ./manage_checklist.sh "$mode" "$path"

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
