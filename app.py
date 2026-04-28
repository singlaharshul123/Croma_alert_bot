import time
import asyncio
from playwright.sync_api import sync_playwright
import requests

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


def check_product(page, url):
    try:
        page.goto(url, timeout=15000)
        content = page.content().lower()

        # ❌ OUT OF STOCK SIGNALS
        if "not available for your pincode" in content:
            return False

        if "notify me" in content and "add to cart" not in content:
            return False

        # ✅ YOUR OBSERVATION BASED SIGNALS
        has_add_to_cart = "add to cart" in content
        has_buy_now = "buy now" in content
        has_delivery = "will be delivered by" in content

        if has_add_to_cart and (has_buy_now or has_delivery):
            return True

        return False

    except:
        return False


print("🚀 Playwright stock bot started...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    while True:
        for pid, name in PRODUCTS.items():
            for pin in PINCODES:

                key = f"{pid}-{pin}"

                if key in sent:
                    continue

                url = f"https://www.croma.com/p/{pid}"

                if check_product(page, url):
                    msg = f"🔥 IN STOCK!\n{name}\nProduct: {pid}\nPincode: {pin}"
                    print(msg)
                    send_telegram(msg)
                    sent.add(key)

        time.sleep(5)
