import time
import requests

BOT_TOKEN = "8293946395:AAHLrBFmcAtWiZDideIMqbDoZnl8W7K8si4"
CHAT_ID = "5007925991"

PRODUCTS = {
    "315715": "Vivo T4 5G",
    "320388": "Redmi Note 15 Pro 5G (8GB/128GB Silver Ash)"
}

PINCODES = ["125120"]

sent = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-IN,en;q=0.9"
}


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=15)
    except Exception as e:
        print("Telegram Error:", e)


def check_stock(pid, pin):
    url = f"https://www.croma.com/p/{pid}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        text = r.text.lower()

        # OUT OF STOCK for pincode
        if "not available for your pincode" in text:
            return False

        # IN STOCK if delivery date visible
        if "will be delivered by" in text:
            return True

        # Backup condition
        if "buy now" in text and "add to cart" in text:
            return True

        # Notify me means usually OOS
        if "notify me" in text:
            return False

        return False

    except Exception as e:
        print("Check Error:", e)
        return False


print("🚀 Bot Started")

while True:
    for pid, name in PRODUCTS.items():
        for pin in PINCODES:
            key = f"{pid}-{pin}"

            print(f"Checking {name} | PIN {pin}")

            if check_stock(pid, pin):
                if key not in sent:
                    msg = f"🔥 IN STOCK ALERT!\n📦 {name}\n📍 PIN: {pin}\n🔗 https://www.croma.com/p/{pid}"
                    send(msg)
                    sent.add(key)
                    print("Alert sent")
                else:
                    print("Already alerted")
            else:
                if key in sent:
                    sent.remove(key)   # re-alert if stock returns later
                print("Still out of stock")

    time.sleep(10)
