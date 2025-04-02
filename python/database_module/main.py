import psycopg2
from dotenv import dotenv_values

config = dotenv_values("./.env")

connection = psycopg2.connect(
    host="localhost",
    database="pg-demo",
    user=config.get('db_user'),
    password=config.get('db_password')
)

cursor = connection.cursor()

create_investments_table = """
create table investments (
    id serial primary key,
    coin varchar(32),
    currency varchar(3),
    amount real
)
"""
# cursor.execute(create_investments_table)


add_investment_template = """
insert into investments (
    coin, currency, amount
) values %s
"""

data = [("bitcoin", "USD", 5.0)]
cursor.execute(add_investment_template, data)


get_investments_template = """
select * from investments where coin = 'bitcoin'
"""
cursor.execute(get_investments_template)
print(cursor.fetchall())


connection.commit()

cursor.close()
connection.close()