import time
import requests

BOT_TOKEN = "8293946395:AAHLrBFmcAtWiZDideIMqbDoZnl8W7K8si4"
CHAT_ID = "5007925991"

PRODUCTS = {
    "315715": "Vivo T4 5G",
    "320388": "Redmi Note 15 Pro 5G (8GB/128GB Silver Ash)"
}

PINCODES = ["125120"]

PINCODES = ["125120"]

sent = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-IN,en;q=0.9"
}

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check_stock(pid, pin):
    url = f"https://www.croma.com/p/{pid}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        text = r.text.lower()

        if "add to cart" in text:
            return True

        if "notify me" in text:
            return False

        return False

    except Exception as e:
        print("Error:", e)
        return False

print("Bot started")

while True:
    for pid, name in PRODUCTS.items():
        for pin in PINCODES:
            key = f"{pid}-{pin}"

            if key in sent:
                continue

            print("Checking", name, pin)

            if check_stock(pid, pin):
                msg = f"🔥 IN STOCK\n{name}\nPIN: {pin}\nhttps://www.croma.com/p/{pid}"
                send(msg)
                sent.add(key)
                print("Alert sent")
            else:
                print("Still out of stock")

    time.sleep(10)
