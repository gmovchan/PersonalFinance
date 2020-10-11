from sqlalchemy import create_engine
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
    moneyDB.to_sql("money", con=engine)

engine = create_engine("sqlite:///C:\\sqlite\\finance.db", echo=False)

moneyDB = pd.read_sql_table("money", engine, index_col="index")
moneyDB = moneyDB[moneyDB["users"] == int(183291591)]
print(moneyDB.iterrows())

result = ""
for index, row in moneyDB.iterrows():
    result += "Date: {}/{}/{}, wallet {} \u20BD, drawer {} \u20BD, bank {} \u20BD\n".format(row['days'], row['months'], \
    row['years'], row['wallet'], row['drawer'], row['bank'])
print(result)