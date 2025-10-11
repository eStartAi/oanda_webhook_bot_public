#!/bin/bash

set -e

if [ "$1" == "sandbox" ]; then
    cp .env.sandbox .env
    echo "🔧 Switched to SANDBOX environment (.env.sandbox → .env)"
elif [ "$1" == "live" ]; then
    cp .env.live .env
    echo "🚀 Switched to LIVE environment (.env.live → .env)"
else
    echo "❌ Usage: ./switch_env.sh [sandbox|live]"
    exit 1
fi
