import os
import requests
from bs4 import BeautifulSoup


def fetch_stock_price(stock_code: str) -> str:
    url = f"https://tw.stock.yahoo.com/quote/{stock_code}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    price_tag = soup.find("span", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"})

    if price_tag is None:
        raise ValueError(
            "無法從頁面上找到股價，可能是頁面結構已改變或需要動態渲染"
        )

    return price_tag.text.strip()


def send_telegram_message(token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, data={
        "chat_id": chat_id,
        "text": text,
    }, timeout=10)
    response.raise_for_status()


if __name__ == "__main__":
    stock_code = "2330"
    price = fetch_stock_price(stock_code)
    message = f"目前股價：{price}"
    print(message)

    token = os.getenv("TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if token and chat_id:
        send_telegram_message(token, chat_id, message)
        print("已傳送 Telegram 訊息。")
    else:
        print("TOKEN 或 CHAT_ID 尚未設定，僅列印股價。")
