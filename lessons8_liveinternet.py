import csv

import requests


def get_server_response(url: str) -> str:
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open("liveinternet.csv", "a", newline="", encoding="utf-8") as f:
        order = ["name", "url", "description", "traffic", "percent"]
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def main():

    for i in range(1, 6834):
        url = f"https://www.liveinternet.ru/rating/ru//today.tsv?page={i}"
        response = get_server_response(url)
        data = response.strip().replace("&quot;", "'").split("\n")[1:]

        for row in data:
            columns = row.strip().split("\t")
            name = columns[0]
            url = columns[1]
            description = columns[2]
            traffic = columns[3]
            percent = columns[4]

            data = {
                "name": name,
                "url": url,
                "description": description,
                "traffic": traffic,
                "percent": percent,
            }
            write_csv(data)


if __name__ == "__main__":
    main()
