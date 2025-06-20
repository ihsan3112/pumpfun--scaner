import os
import requests
from bs4 import BeautifulSoup
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
sent_tokens = set()

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Failed to send message: {e}")

def fetch_tokens():
    url = "https://pump.fun/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers)
        print("Status code:", response.status_code)
        print("Response length:", len(response.text))

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        print(f"Total link ditemukan: {len(links)}")

        for link in links:
            href = link["href"]
            if href.startswith("/token/"):
                full_url = "https://pump.fun" + href
                if full_url not in sent_tokens:
                    sent_tokens.add(full_url)
                    send_to_telegram(f"Token baru ditemukan!\n{full_url}")
                    print("Dikirim:", full_url)

    except Exception as e:
        print(f"Fetch error: {e}")

if __name__ == "__main__":
    while True:
        fetch_tokens()
        time.sleep(20)
