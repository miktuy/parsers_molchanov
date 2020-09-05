import csv
from dataclasses import dataclass
from typing import Iterable


import requests
from bs4 import BeautifulSoup


WP_PLUGINS_URL = "https://wordpress.org/plugins/browse/blocks/"


@dataclass
class Plugin(Iterable):
    name: str
    author: str

    def __iter__(self):
        return iter((self.name, self.author))


def write_csv(data: Plugin):
    with open("plugins_authors.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def parse_page(page: BeautifulSoup):
    articles = page.find_all("article", class_="plugin-card")
    for article in articles:
        name = article.find("div", class_="entry").find("h3", class_="entry-title").text
        author = (
            article.find("footer")
            .find("span", class_="plugin-author")
            .text.encode("ascii", errors="replace")
            .decode()
            .strip()
        )
        data = Plugin(name=name, author=author)
        write_csv(data)


def get_data(html: str):
    page = BeautifulSoup(html, "lxml")
    parse_page(page)


def get_pages_numbers(main_page_url: str) -> int:
    html = get_html(main_page_url)
    soup = BeautifulSoup(html, "lxml")
    last_page = (
        soup.find("main", id="main")
        .find("div", class_="nav-links")
        .find_all("a", class_="page-numbers")[-2]
        .text
    )
    return int(last_page)


def get_html(url: str) -> str:
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def main():
    page_numbers = get_pages_numbers(WP_PLUGINS_URL)
    for i in range(1, page_numbers + 1):
        url = f"{WP_PLUGINS_URL}page/{i}"
        get_data(get_html(url=url))


if __name__ == "__main__":
    main()
