import csv
import re
from typing import Optional


import requests
from bs4 import BeautifulSoup


from lesson3 import CoinRow


COINMARKETCUP_URL = "https://coinmarketcap.com"
NEXT_PATTERN = re.compile("Next")


def get_html(url: str) -> Optional[str]:
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def write_csv(data: CoinRow):
    with open("coinmarketcap.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def get_page_data(html: str):
    soup = BeautifulSoup(html, "lxml")
    trs = soup.find_all("table")[2].find("tbody").find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) > 1:
            name = tds[1].find("a").text
            ticker = tds[5].find("div").text.split(" ")[1]
            url = COINMARKETCUP_URL + tds[1].find("a").get("href")
            try:
                price = float(tds[3].find("a").text.replace("$", "").replace(",", ""))
            except:
                price = None
            crypto = CoinRow(name, ticker, url, price)
            write_csv(crypto)


def is_next_page_exists(html: str) -> bool:
    soup = BeautifulSoup(html, "lxml")
    next_btn = soup.find("a", text=NEXT_PATTERN)
    return next_btn is not None


def get_next_href(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    next_btn = soup.find("a", text=NEXT_PATTERN)
    return next_btn.get("href")


def main():
    url = COINMARKETCUP_URL
    while True:
        html = get_html(url)
        get_page_data(html)
        if is_next_page_exists(html):
            url = f"{COINMARKETCUP_URL}{get_next_href(html)}"
        else:
            break


if __name__ == "__main__":
    main()
