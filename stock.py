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


if __name__ == "__main__":
    stock_code = "2330"
    price = fetch_stock_price(stock_code)
    print(f"目前股價：{price}")
