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
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check(pid, pin):
    url = f"https://www.croma.com/p/{pid}"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-IN,en;q=0.9"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.text.lower()

        # ❌ OUT OF STOCK
        if "not available for your pincode" in data:
            return False

        if "notify me" in data and "add to cart" not in data:
            return False

        # ✅ IN STOCK
        if "add to cart" in data:
            return True

        if "will be delivered" in data:
            return True

        return False

    except Exception as e:
        print("Error:", e)
        return False


print("🚀 FINAL BOT RUNNING")

while True:
    for pid, name in PRODUCTS.items():
        for pin in PINCODES:

            key = f"{pid}-{pin}"

            if key in sent:
                continue

            print(f"Checking {pid} {pin}")

            if check(pid, pin):
                msg = f"🔥 IN STOCK!\n{name}\n{pid} ({pin})"
                print(msg)
                send(msg)
                sent.add(key)

    time.sleep(5)
