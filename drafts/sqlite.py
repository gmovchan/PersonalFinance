'''from sqlalchemy import create_engine
from random import randrange
import pandas as pd

def fillDB():
    moneyDB = pd.DataFrame.from_dict({"users": [], "years": [], "months": [], "days": [], "wallet": [], "drawer": [],
                                      "bank": []}).astype("int64")

    users = [771637784, 760305618, 921123602, 560227159, 968638050, 183291591]

    for x in range(31):
        moneyDB = moneyDB.append({"users": users[randrange(0, 6)], "years": randrange(2016, 2020), "months":
            randrange(1, 13), "days": randrange(1, 32), "wallet": randrange(0, 1000), "drawer": randrange(0, 1000),
                                  "bank":
                                      randrange(0, 1000)}, ignore_index=True)

    engine = create_engine("sqlite:///C:\\sqlite\\finance.db", echo=False)
    moneyDB.to_sql("money", con=engine, if_exists="replace")

    return True

engine = create_engine("sqlite:///C:\\sqlite\\finance.db", echo=False)

fillDB()'''
'''moneyDB = pd.read_sql_table("money", engine, index_col="index")
moneyDB = moneyDB[moneyDB["users"] == int(183291591)]
print(moneyDB.iterrows())

result = ""
for index, row in moneyDB.iterrows():
    result += "Date: {}/{}/{}, wallet {} \u20BD, drawer {} \u20BD, bank {} \u20BD\n".format(row['days'], row['months'], \
    row['years'], row['wallet'], row['drawer'], row['bank'])
print(result)'''

from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.sql import select
engine = create_engine("sqlite:///finance.db", echo=False)
meta = MetaData()
'''tb1 = Table("tb1", meta, autoload=True, autoload_with=engine)
print([c.name for c in tb1.columns])
with engine.begin() as connection:
    r1 = connection.execute(tb1.select())
    connection.execute(tb1.insert(), {"username": "Jhon", "age": "27"})'''

moneyTb = Table("money", meta, autoload=True, autoload_with=engine)
print([c.name for c in moneyTb.columns])
with engine.begin() as connection:
    s = select([moneyTb]).where(moneyTb.c.unique_id == 3)
    print(len(connection.execute(s).fetchall()))
    #r1 = connection.execute(moneyTb.select())
    #connection.execute(moneyTb.insert(), {"users": 183291591, "years": 2020, "months": 12, "days": 1, "wallet": 100, "drawer": 200, "bank": 300})
    #stmt = moneyTb.update().where(moneyTb.c.unique_id == 1).values(wallet=999)
    #connection.execute(stmt)