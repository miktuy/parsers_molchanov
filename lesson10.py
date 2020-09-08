import csv
from typing import List

import requests
from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    r = requests.get(url, headers=user_agent)
    return r.text


def write_csv(data: dict):
    with open("catertrax.csv", "a", newline="", encoding="utf-8") as f:
        order = ["author", "since"]
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_articles(html: str) -> list:
    soup = BeautifulSoup(html, "lxml")
    ts = soup.find("div", class_="testimonial-container").find_all("article")
    return ts


def get_review(articles: List[BeautifulSoup]):
    for article in articles:
        try:
            since = article.find("p", class_="traxer-since").text.strip()
        except:
            since = ""
        try:
            author = article.find("p", class_="testimonial-author").text.strip()
        except:
            author = ""
        data = {"author": author, "since": since}
        write_csv(data)


def main():
    # 1. Get container with reviews and list with reviews
    # 2. If list exists than parse reviews
    #    else - break the loop

    page = 1
    while True:
        url = "https://catertrax.com/why-catertrax/traxers/page/{}/".format(str(page))

        articles = get_articles(get_html(url))
        if articles:
            page += 1
            get_review(articles)
        else:
            break


if __name__ == "__main__":
    main()
