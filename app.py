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
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        print("Telegram failed to send")

def check_stock(page, pid, pin):
    try:
        # Check for the common "Out of Stock" button
        is_notify = page.locator("button:has-text('Notify Me')").is_visible()
        is_add_to_cart = page.locator("button:has-text('Add to Cart')").is_visible()
        
        # Croma specific: Sometimes the button is there but 'Delivery' says not available
        not_serviceable = page.locator("text=Not Available for your pincode").is_visible()

        if is_add_to_cart and not not_serviceable:
            return True
        return False
    except:
        return False

print("🚀 BOT DEPLOYED ON RAILWAY - MONITORING START")

with sync_playwright() as p:
    # Use a real-looking User Agent to avoid bot detection
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    
    while True:
        for pid, name in PRODUCTS.items():
            for pin in PINCODES:
                key = f"{pid}-{pin}"
                if key in sent: continue

                # Fresh context for each check to ensure Pincode actually updates
                context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                page = context.new_page()
                
                try:
                    url = f"https://www.croma.com/p/{pid}"
                    print(f"🔍 Checking {name} ({pid}) for Pin: {pin}")
                    
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    time.sleep(4) # Allow JS to load

                    # Improved Pincode Entry
                    try:
                        # Click the pincode display area
                        page.click(".pincode-serviceability", timeout=5000)
                        page.fill("#pincode", pin) # Use the actual ID if known, or generic
                        page.press("#pincode", "Enter")
                        time.sleep(3)
                    except:
                        pass # If already set or selector changed

                    if check_stock(page, pid, pin):
                        msg = f"🔥 IN STOCK ALERT!\n📦 {name}\n📍 Pincode: {pin}\n🔗 https://www.croma.com/p/{pid}"
                        print(msg)
                        send(msg)
                        sent.add(key)
                    else:
                        print(f"❌ {pid} Out of Stock for {pin}")

                except Exception as e:
                    print(f"⚠️ Page error on {pid}: {e}")
                
                page.close()
                context.close()
        
        print("Waiting 60 seconds for next cycle...")
        time.sleep(60) # Don't spam too fast or Croma will ban your IP
