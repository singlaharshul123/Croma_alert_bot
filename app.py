import time
import requests

# =========================
# TELEGRAM SETTINGS
# =========================
BOT_TOKEN = "8293946395:AAHLrBFmcAtWiZDideIMqbDoZnl8W7K8si4"
CHAT_ID = "5007925991"

# =========================
# PRODUCTS
# =========================
PRODUCTS = {
    "315715": "Vivo T4 5G",
    "320388": "Redmi Note 15 Pro 5G"
}

# =========================
# PINCODE
# =========================
PINCODE = "125120"

# =========================
# HEADERS
# =========================
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-IN,en;q=0.9"
}

# Avoid duplicate alerts
sent = set()

# =========================
# TELEGRAM MESSAGE
# =========================
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

# =========================
# CHECK STOCK
# =========================
def check_stock(pid):
    try:
        url = f"https://www.croma.com/p/{pid}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        text = r.text.lower()

        # Detect analytics stock tag
        if "v1in_stock" in text:
            return True

        # Detect Add to cart button
        if "add to cart" in text:
            return True

        return False

    except Exception as e:
        print("Error:", e)
        return False

# =========================
# MAIN LOOP
# =========================
print("🚀 Croma Bot Started")

while True:
    for pid, name in PRODUCTS.items():

        print("Checking:", name)

        in_stock = check_stock(pid)

        if in_stock:
            if pid not in sent:
                msg = f"""🔥 IN STOCK ALERT

{name}
Pincode: {PINCODE}

https://www.croma.com/p/{pid}
"""
                send(msg)
                sent.add(pid)
                print("Alert sent")

        else:
            print("Still out of stock")

            # reset when out of stock again
            if pid in sent:
                sent.remove(pid)

    time.sleep(10)
