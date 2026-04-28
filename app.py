import requests
import time

BOT_TOKEN = "8293946395:AAHLrBFmcAtWiZDideIMqbDoZnl8W7K8si4"
CHAT_ID = "5007925991"

PRODUCT_CODE = "322042"
PINCODE = "110001"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Telegram error:", e)

def check_stock():
    url = f"https://www.croma.com/api/v2/product/{PRODUCT_CODE}?pincode={PINCODE}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.text.lower()

        if "out of stock" in data:
            return False

        if "add to cart" in data or "buy now" in data:
            return True

        return False

    except Exception as e:
        print("Request error:", e)
        return False


print("🚀 Started checking...")

while True:
    if check_stock():
        print("✅ FOUND IN STOCK!")
        send_telegram(f"🔥 IN STOCK!\nProduct Code: {PRODUCT_CODE}")
        break
    else:
        print("⏳ checking...")

    time.sleep(5)
