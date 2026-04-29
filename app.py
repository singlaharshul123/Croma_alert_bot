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

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        print("Telegram error")

def check(pid, pin):
    url = f"https://www.croma.com/api/v2/product/{pid}?pincode={pin}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.text.lower()

        print(f"Checking {pid} {pin}")

        # DEBUG print
        print(data[:200])  

        if "out of stock" in data:
            return False

        if "add to cart" in data:
            return True

        return False

    except Exception as e:
        print("Error:", e)
        return False


print("🚀 Bot started...")

while True:
    for pid, name in PRODUCTS.items():
        for pin in PINCODES:

            key = f"{pid}-{pin}"

            if key in sent:
                continue

            if check(pid, pin):
                msg = f"🔥 IN STOCK!\n{name}\n{pid} ({pin})"
                print(msg)
                send(msg)
                sent.add(key)

    time.sleep(5)
