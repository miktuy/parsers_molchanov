import requests
import csv
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Plugin:
    name: str
    url: str
    rating: int

    def __iter__(self):
        return iter((self.name, self.url, self.rating))


def get_html(url: str) -> str:
    r = requests.get(url)
    return r.text


def refined(row_string: str) -> int:
    r = row_string.split()[0].replace(",", "")
    return int(r)


def write_csv(data: Plugin):
    with open("plugins.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def get_data(html: str):
    soup = BeautifulSoup(html, "lxml")
    popular = soup.find_all("section")[1]
    plugins = popular.find_all("article")

    for plugin in plugins:
        name = plugin.find("h3").text
        url = plugin.find("h3").find("a").get("href")
        rating_string = plugin.find("span", class_="rating-count").find("a").text
        rating = refined(rating_string)
        data = Plugin(name, url, rating)
        write_csv(data)

    return None


def main():
    url = "https://wordpress.org/plugins/"
    print(get_data(get_html(url)))


if __name__ == "__main__":
    main()
