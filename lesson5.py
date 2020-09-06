import csv


def write_csv(data: dict):
    with open("names.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(data.values())


def write_csv_2(data: dict):
    with open("names.csv", "a") as f:
        order = ["name", "surname", "age"]
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def main():
    d = {"name": "Petr", "surname": "Ivanov", "age": 20}
    d1 = {"name": "Anton", "surname": "Smirnov", "age": 30}
    d2 = {"name": "Semen", "surname": "Petrov", "age": 40}

    l = [d, d1, d2]

    with open("cmc.csv") as f:
        order = ["name", "ticker", "url", "price"]
        reader = csv.DictReader(f, fieldnames=order)
        for row in reader:
            print(dict(row))


if __name__ == "__main__":
    main()
