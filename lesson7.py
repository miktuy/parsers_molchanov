import csv
from dataclasses import dataclass


import peewee as pw


DB_INSERT_STEP = 10


db = pw.PostgresqlDatabase(
    database="test", user="postgres", password="p4ssw0rd", host="localhost", port=4902
)


# @dataclass
class Coin(pw.Model):
    name = pw.CharField()
    ticker = pw.CharField(max_length=12)
    url = pw.TextField()
    price = pw.CharField()

    class Meta:
        database = db


def read_from_csv(file="cmc.csv"):
    with open(file) as f:
        order = ["name", "ticker", "url", "price"]
        reader = csv.DictReader(f, fieldnames=order)

        return list(reader)


def main():
    db.connect()
    db.create_tables([Coin])
    coins = read_from_csv()

    # Slow dummy solve for db writing
    # for item in coins:
        # coin = Coin(
        #     name=item["name"], ticker=item["ticker"], url=item["url"], price=item["price"]
        # )
        # coin.save()

    # Used transactions
    # with db.atomic():
    #     for row in coins:
    #         Coin.create(**row)

    # Used index and slices
    with db.atomic():
        for index in range(0, len(coins), DB_INSERT_STEP):
            Coin.insert_many(coins[index:index+DB_INSERT_STEP]).execute()


if __name__ == "__main__":
    main()
