# PersonalFinance
This app is supposed to help with keeping track of money in different places, such as a pocket, a bank account, a drawer and
 so on.

The app has an embedded telegram bot that should be available at the link https://t.me/money_buckets_bot

The script requires a LiteSQL database named finance.db containing a table named money made out of a following SQL 
query:

    CREATE TABLE money (
      unique_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      users INTEGER NOT NULL,
      years INTEGER NOT NULL,
      months INTEGER NOT NULL,
      days INTEGER NOT NULL,
      wallet INTEGER NOT NULL,
      drawer INTEGER NOT NULL,
      bank INTEGER NOT NULL
    );