#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./manage_checklist.sh [live|practice] now"
    exit 1
fi

mode=$1
param=$2

if [ "$param" == "now" ]; then
    # find latest backup file in backups/
    latest=$(ls -t backups/backup_* | head -n 1)
else
    latest="$param"
fi

echo "📦 Latest backup: $latest"

python3 update_checklist.py "$mode" "$latest"
