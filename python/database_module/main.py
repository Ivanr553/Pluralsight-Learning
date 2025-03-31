import requests, click, sqlite3
from datetime import datetime

from constants import *


def get_coin_price(coin_id, currency):
    try:
        response = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
        )

        if response.status_code == 200:
            data = response.json()
            return data[coin_id][currency]
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    except Exception:
        print(f"Got this error: {Exception.args[0]}")
        return None


@click.group()
def cli():
    pass


@cli.command()
@click.option("--coin_id", default="bitcoin")
@click.option("--currency", default="usd")
def show_coin_price(coin_id, currency):
    price = get_coin_price(coin_id, currency)
    print(f"The price of {coin_id} in {currency} is {price}")


@cli.command()
@click.option("--coin_id", default="bitcoin")
@click.option("--currency", default="usd")
@click.option("--amount", type=float)
@click.option("--sell", is_flag=True, default=False)
def add_investment(coin_id, currency, amount, sell):
    price = get_coin_price(coin_id, currency)
    database = sqlite3.connect("./database/test.db")
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO investments (coin_id, currency, amount, sell, date) VALUES (?, ?, ?, ?, ?)",
        (coin_id, currency, amount, sell, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    database.commit()

    if sell:
        print(f"You sold {amount} {coin_id} for {amount * price} {currency}")
    else:
        print(f"You bought {amount} {coin_id} for {amount * price} {currency}")


cli.add_command(show_coin_price)
cli.add_command(add_investment)

if __name__ == "__main__":
    database = sqlite3.connect("./database/test.db")
    cursor = database.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS investments (coin_id TEXT, currency TEXT, amount REAL, sell BOOLEAN, date TEXT)"
    )
    cli()
