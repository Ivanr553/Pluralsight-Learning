from dataclasses import dataclass
import requests, click, sqlite3
from datetime import datetime

from constants import *

@dataclass
class Investment:
    coin_id: str
    currency: str
    amount: int
    sell: bool
    date: datetime
    
    def compute_value(self) -> float:
        return self.amount * get_coin_price(self.coin_id, self.amount)
    
def investment_row_factory(_, row):
    return Investment(
        coin_id= row[0],
        currency= row[1],
        amount= row[2],
        sell= row[3],
        date= datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
    )

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
@click.option("--coin_id")
@click.option("--currency", default="usd")
@click.option("--amount", type=float)
@click.option("--sell", is_flag=True, default=False)
def add_investment(coin_id, currency, amount, sell):
    price = get_coin_price(coin_id, currency)
    database = sqlite3.connect("./databases/test.db")
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


@cli.command()
def get_all_investments():
    cursor = database.cursor()
    cursor.execute("select * from investments;")
    rows = cursor.fetchall()
    for row in rows:
        print(row.coin_id, row.amount, row.sell, row.date)
    
@cli.command()
@click.option("--coin_id")
@click.option("--currency")
def get_current_investment_value(coin_id, currency):
    cursor = database.cursor()
    buy_rows = cursor.execute("select * from investments  where coin_id=? and currency=? and sell=?", (coin_id, currency, False)).fetchall()
    sell_rows = cursor.execute("select * from investments  where coin_id=? and currency=? and sell=?", (coin_id, currency, True)).fetchall()
    buys = sum([row.amount for row in buy_rows])
    sells = sum([row.amount for row in sell_rows])
    total_amount = buys - sells
    value = get_coin_price(coin_id, currency) * total_amount
    print(f"The current value of your {coin_id} investment is {value} {currency}")
    

cli.add_command(show_coin_price)
cli.add_command(add_investment)
cli.add_command(get_all_investments)
cli.add_command(get_current_investment_value)

if __name__ == "__main__":
    database = sqlite3.connect("./databases/test.db")
    database.row_factory = investment_row_factory
    cursor = database.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS investments (coin_id TEXT, currency TEXT, amount REAL, sell BOOLEAN, date TEXT)"
    )
    cli()
