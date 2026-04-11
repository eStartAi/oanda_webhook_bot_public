> Last reset: 2026-04-11 20:00:08 UTC by GitHub Actions

# 🔐 Safe Go-Live Checklist (Live Crypto Trading - Kraken)

Use this checklist before switching to **Kraken LIVE API mode**.

---

## ✅ Today's Backup Summary
- [x] Backup created: backups/backup_20260411_160001
- [x] `.env` synced safely and verified

## 🔒 Security
- [ ] `.env` contains LIVE Kraken API keys
- [ ] Telegram kill-switch working
- [ ] Trade size logic confirmed with live balance

## 🚨 Risk Control
- [ ] Max trades/day enabled
- [ ] Trailing SL & TP logic tested
- [ ] Dry run completed before live

## 🧠 Signal Quality
- [ ] Confidence scoring working (RSI + MACD + Volume Spike)
- [ ] Score-based position sizing confirmed

## 🛠 Infra & Monitoring
- [ ] Logs writing to `logs/`
- [ ] Telegram alerts ✅
- [ ] UptimeRobot / heartbeat monitoring `/health`
- [ ] Trade logs: `trade_log.jsonl` or DB active
- [ ] `auto_close.py` set for EOD

✅ If all boxes are checked, go live with ScaleViper 🐍🔥
