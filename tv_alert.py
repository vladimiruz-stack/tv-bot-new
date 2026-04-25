import requests

BOT_TOKEN = "ВСТАВЬ_ТОКЕН"
CHAT_ID = "38908105"

r = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    json={"chat_id": CHAT_ID, "text": "ТЕСТ 🚀"},
    timeout=20
)

print("STATUS:", r.status_code)
print("RESPONSE:", r.text)
