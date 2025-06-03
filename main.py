import requests
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

sent_tokens = set()

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Failed to send message: {e}")

def fetch_tokens():
    url = "https://pump.fun/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            if href.startswith("/token/"):
                full_url = "https://pump.fun" + href
                if full_url not in sent_tokens:
                    sent_tokens.add(full_url)
                    send_to_telegram(f"Token baru ditemukan!\n{full_url}")
                    print(f"Dikirim: {full_url}")
    except Exception as e:
        print(f"Fetch error: {e}")

if __name__ == "__main__":
    while True:
        fetch_tokens()
        time.sleep(20)

