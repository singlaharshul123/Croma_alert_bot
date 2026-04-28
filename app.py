import requests
import time

BOT_TOKEN = "8293946395:AAHLrBFmcAtWiZDideIMqbDoZnl8W7K8si4"
CHAT_ID = "5007925991"

PRODUCTS = {
    "315715": "Vivo T4 5G",
    "321832": "Nothing Phone 4a 5G"
}

PINCODES = ["125120", "126116"]

sent = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass


def check_stock(product_id, pin):
    url = f"https://www.croma.com/p/{product_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text.lower()

        # REAL SIGNALS (Croma page behavior)
        if "add to cart" in html:
            return True

        if "notify me" in html and "out of stock" in html:
            return False

        if "out of stock" in html:
            return False

        return False

    except:
        return False


print("🚀 Stock bot started...")

while True:
    for pid, name in PRODUCTS.items():
        for pin in PINCODES:

            key = f"{pid}-{pin}"

            if key in sent:
                continue

            if check_stock(pid, pin):
                msg = f"🔥 IN STOCK!\n{name}\nProduct ID: {pid}\nPincode: {pin}"
                print(msg)
                send_telegram(msg)
                sent.add(key)

    time.sleep(5)
