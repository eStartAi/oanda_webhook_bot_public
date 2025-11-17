import requests

TOKEN = "7695215773:AAF5ijRy1NvZgVsYAWR6m9sOlZcNvRSAWR8"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(url)
print("📥 Raw Response:", response.text)

try:
    updates = response.json()
    for result in updates["result"]:
        message = result.get("message") or result.get("channel_post")
        if message:
            print("✅ Your Chat ID is:", message["chat"]["id"])
except Exception as e:
    print("❌ Error parsing chat ID:", e)
