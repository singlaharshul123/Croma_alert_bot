import time
import requests
from playwright.sync_api import sync_playwright

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

def check_stock(page):
    try:
        # ❌ OUT OF STOCK signals
        if page.locator("text=Not Available for your pincode").count() > 0:
            return False

        if page.locator("text=Notify Me").count() > 0 and page.locator("text=Add to Cart").count() == 0:
            return False

        # ✅ IN STOCK signals
        add = page.locator("text=Add to Cart").count()
        buy = page.locator("text=Buy Now").count()
        delivery = page.locator("text=Will be delivered").count()

        print(f"Add:{add} Buy:{buy} Delivery:{delivery}")

        if add > 0 and (buy > 0 or delivery > 0):
            return True

        return False

    except Exception as e:
        print("Error:", e)
        return False


print("🚀 FINAL BOT RUNNING")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context()
    page = context.new_page()

    while True:
        for pid, name in PRODUCTS.items():
            for pin in PINCODES:

                key = f"{pid}-{pin}"

                if key in sent:
                    continue

                url = f"https://www.croma.com/p/{pid}"

                try:
                    print(f"Checking {pid} {pin}")

                    page.goto(url, timeout=30000)
                    time.sleep(3)

                    # try setting pincode
                    try:
                        page.click("text=Check Delivery", timeout=5000)
                        page.fill("input[type='tel']", pin)
                        page.keyboard.press("Enter")
                        time.sleep(2)
                    except:
                        pass

                    if check_stock(page):
                        msg = f"🔥 IN STOCK!\n{name}\n{pid} ({pin})"
                        print(msg)
                        send(msg)
                        sent.add(key)

                except Exception as e:
                    print("Page error:", e)

        time.sleep(5)
