import time
import requests
import re
import json

BOT_TOKEN = "8293946395:AAHLrBFmcAtWiZDideIMqbDoZnl8W7K8si4"
CHAT_ID = "5007925991"

PRODUCTS = {
    "315715": "Vivo T4 5G",
    "320388": "Redmi Note 15 Pro 5G"
}

PINCODE = "125120"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-IN,en;q=0.9"
}

sent = set()


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def check_stock(pid):
    try:
        url = f"https://www.croma.com/p/{pid}"
        r = requests.get(url, headers=HEADERS, timeout=20)
        html = r.text

        # ========= EXACT MATCH FROM PAGE =========
        # Google analytics stock field
        if "stock_status~v1in_stock" in html:
            return True

        if '"stock_status":"in_stock"' in html.lower():
            return True

        if '"stockStatus":"IN_STOCK"' in html:
            return True

        # Buy now means stock
        if "Buy Now" in html:
            return True

        # Add to cart means stock
        if "Add to Cart" in html:
            return True

        # Delivery available means stock
        if "will be delivered by" in html.lower():
            return True

        return False

    except Exception as e:
        print("Error:", e)
        return False


print("🚀 FINAL CROMA BOT RUNNING")

while True:
    for pid, name in PRODUCTS.items():

        print(f"Checking {name} | PIN {PINCODE}")

        stock = check_stock(pid)

        if stock:
            print("🔥 IN STOCK")

            if pid not in sent:
                msg = f"""🔥 CROMA STOCK ALERT

{name}
PINCODE: {PINCODE}

https://www.croma.com/p/{pid}
"""
                send(msg)
                sent.add(pid)

        else:
            print("Still out of stock")

            if pid in sent:
                sent.remove(pid)

    time.sleep(10)
