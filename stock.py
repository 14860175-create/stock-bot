import os
import requests


def fetch_stock_price(stock_code: str) -> str:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_code}.TW"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/javascript, */*; q=0.01"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    try:
        return data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    except (KeyError, IndexError, TypeError):
        raise ValueError("抓不到股價，請確認股票代碼是否正確")


def send_telegram_message(token: str, chat_id: str, text: str) -> requests.Response:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, data={
        "chat_id": chat_id,
        "text": text,
    }, timeout=10)
    return response


if __name__ == "__main__":
    stock_code = "2330"
    try:
        price = fetch_stock_price(stock_code)
        message = f"目前股價：{price}"
        print(message)

        token = os.getenv("TOKEN")
        chat_id = os.getenv("CHAT_ID")
        print("TOKEN =", token)
        print("CHAT_ID =", chat_id)

        if token and chat_id:
            response = send_telegram_message(token, chat_id, message)
            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)
            response.raise_for_status()
            print("已傳送 Telegram 訊息。")
        else:
            print("TOKEN 或 CHAT_ID 尚未設定，僅列印股價。")
    except requests.RequestException as exc:
        print(f"網路請求失敗：{exc}")
    except ValueError as exc:
        print(f"資料解析失敗：{exc}")
    except Exception as exc:
        print(f"發生未知錯誤：{exc}")
