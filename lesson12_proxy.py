import random

import requests
from bs4 import BeautifulSoup


PROXIES_PROVIDER_URL = "https://free-proxy-list.net/"


def get_request(url: str) -> str:
    p = get_proxy()
    proxy = {p["schema"]: p["address"]}
    r = requests.get(url, proxies=proxy, timeout=5)
    return r


def get_proxy():
    html = requests.get(PROXIES_PROVIDER_URL).text
    soup = BeautifulSoup(html, "lxml")
    trs = (
        soup.find("section", id="list")
        .find("div", class_="table-responsive")
        .find("table", class_="table-bordered")
        .find("tbody")
        .find_all("tr")[:20]
    )
    proxies = get_proxies_from_table(trs)
    return random.choice(proxies)


def get_proxies_from_table(trs):
    proxies = []
    for tr in trs:
        tds = tr.find_all("td")
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = "https" if "yes" in tds[6].text.strip() else "http"
        proxy = {"address": f"{ip}:{port}", "schema": schema}
        proxies.append(proxy)
    return proxies


def main():
    print(get_request("http://httpbin.org/ip").json()["origin"])


if __name__ == "__main__":
    main()
