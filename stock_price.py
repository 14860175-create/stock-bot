import argparse
import requests


def fetch_stock_price(stock_code: str) -> str:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_code}.TW"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    try:
        return data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    except (KeyError, IndexError, TypeError):
        raise ValueError("抓不到股價，請確認股票代碼是否正確")


def send_telegram_message(token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, data={
        "chat_id": chat_id,
        "text": text,
    }, timeout=10)
    response.raise_for_status()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="擷取 Yahoo 股市即時股價")
    parser.add_argument("stock_code", nargs="?", default="2330", help="股票代碼，預設為 2330")
    parser.add_argument("--telegram-token", dest="telegram_token", help="Telegram bot token")
    parser.add_argument("--telegram-chat-id", dest="telegram_chat_id", help="Telegram chat_id")
    args = parser.parse_args()

    try:
        price = fetch_stock_price(args.stock_code)
        message = f"目前股價：{price}"
        print(message)

        if args.telegram_token and args.telegram_chat_id:
            send_telegram_message(args.telegram_token, args.telegram_chat_id, message)
            print("已傳送 Telegram 訊息。")
        elif args.telegram_token or args.telegram_chat_id:
            print("請同時提供 --telegram-token 和 --telegram-chat-id 才能發送 Telegram 訊息。")
    except requests.RequestException as exc:
        print(f"網路請求失敗：{exc}")
    except ValueError as exc:
        print(f"資料解析失敗：{exc}")
    except Exception as exc:
        print(f"發生未知錯誤：{exc}")
