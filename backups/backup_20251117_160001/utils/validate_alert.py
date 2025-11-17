kprovided_secret = str(data.get("secret", "")).strip()
expected_secret = str(os.getenv("WEBHOOK_SECRET", "")).strip()

print(f"🔑 Comparing secrets: provided='{provided_secret}' expected='{expected_secret}'")

if provided_secret != expected_secret:
    return False, "Invalid webhook secret"

