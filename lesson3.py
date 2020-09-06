import csv
from dataclasses import dataclass
from typing import Iterable, Optional

import requests
from bs4 import BeautifulSoup


COINMARKET_URL = "https://coinmarketcap.com/"


@dataclass
class CoinRow(Iterable):
    name: str
    ticker: str
    url: str
    price: Optional[float]

    def __iter__(self):
        return iter((self.name, self.ticker, self.url, self.price))


def get_html(url: str) -> str:
    return requests.get(url).text


def write_csv(data: CoinRow):
    with open("cmc.csv", "a", newline='') as f:
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
            url = COINMARKET_URL + tds[1].find("a").get("href")
            price = float(tds[3].find("a").text.replace("$", "").replace(",", ""))
            crypto = CoinRow(name, ticker, url, price)
            print(crypto)
            write_csv(crypto)


def main():
    url = COINMARKET_URL
    print(get_page_data(get_html(url=url)))


if __name__ == "__main__":
    main()
