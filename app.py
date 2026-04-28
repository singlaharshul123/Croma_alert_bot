import requests
import time

BOT_TOKEN = "8293946395:AAHLrBFmcAtWiZDideIMqbDoZnl8W7K8si4"   # apna real token yahan dalna
CHAT_ID = "5007925991"

PRODUCT_CODES = ["322042", "321832", "322046"]
PINCODE = "110001"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Telegram error:", e)

def check_stock(product_code):
    url = f"https://www.croma.com/api/v2/product/{product_code}?pincode={PINCODE}"
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


print("🚀 Started multi-product checking...")

while True:
    for code in PRODUCT_CODES:
        if check_stock(code):
            print("✅ FOUND:", code)
            send_telegram(f"🔥 IN STOCK!\nProduct Code: {code}")
            time.sleep(10)  # spam avoid
    else:
        print("⏳ checking...")

    time.sleep(5)
