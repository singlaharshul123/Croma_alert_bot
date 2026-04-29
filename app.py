import requests
import os

BOT_TOKEN = os.getenv("8293946395:AAHLrBFmcAtWiZDideIMqbDoZnl8W7K8si4")
CHAT_ID = os.getenv("5007925991")

PRODUCTS = {
    "320388": "Redmi Note 15 Pro 5G",
    "322042": "Vivo Y11 5G"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-IN,en;q=0.9"
}

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check_stock(pid):
    url = f"https://www.croma.com/p/{pid}"
    r = requests.get(url, headers=HEADERS, timeout=20)
    text = r.text.lower()

    positive = [
        "add to cart",
        "buy now",
        "will be delivered by",
        "in_stock",
        "stock_status~v1in_stock"
    ]

    negative = [
        "not available for your pincode",
        "notify me",
        "out of stock"
    ]

    score = 0

    for x in positive:
        if x in text:
            score += 1

    for x in negative:
        if x in text:
            score -= 2

    return score >= 2

for pid, name in PRODUCTS.items():
    try:
        print("Checking", name)

        if check_stock(pid):
            send(f"🔥 IN STOCK\n{name}\nhttps://www.croma.com/p/{pid}")
            print("Alert sent")

        else:
            print("Still out of stock")

    except Exception as e:
        print("Error:", e)
