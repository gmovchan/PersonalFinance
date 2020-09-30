import pandas as pd
from datetime import date
from datetime import time
#from IPython.display import clear_output

moneyDB = pd.DataFrame.from_dict({"years": [], "months": [], "days": [], "wallet": [], "drawer": [],
                                  "bank": []}).astype("int64")
cleanedMoneyDB = moneyDB.copy()

moneyDB = moneyDB.append({"years": 2020, "months": 8, "days": 31, "wallet": 100, "drawer": 100, "bank": 100}, 
                         ignore_index=True)
moneyDB = moneyDB.append({"years": 2020, "months": 8, "days": 30, "wallet": 200, "drawer": 200, "bank": 200}, 
                         ignore_index=True)
moneyDB = moneyDB.append({"years": 2020, "months": 9, "days": 10, "wallet": 300, "drawer": 300, "bank": 300}, 
                         ignore_index=True)
moneyDB = moneyDB.append({"years": 2020, "months": 9, "days": 15, "wallet": 400, "drawer": 400, "bank": 400}, 
                         ignore_index=True)
moneyDB = moneyDB.append({"years": 2020, "months": 7, "days": 5, "wallet": 300, "drawer": 300, "bank": 300}, 
                         ignore_index=True)
moneyDB = moneyDB.append({"years": 2020, "months": 7, "days": 17, "wallet": 400, "drawer": 400, "bank": 400}, 
                         ignore_index=True)
moneyDB = moneyDB.append({"years": 2020, "months": 7, "days": 18, "wallet": 400, "drawer": 400, "bank": 400}, 
                         ignore_index=True)
moneyDB = moneyDB.append({"years": 2020, "months": 6, "days": 5, "wallet": 400, "drawer": 400, "bank": 400}, 
                         ignore_index=True)
moneyDB = moneyDB.append({"years": 2019, "months": 6, "days": 25, "wallet": 500, "drawer": 500, "bank": 500}, 
                         ignore_index=True)
moneyDB = moneyDB.append({"years": 2019, "months": 7, "days": 25, "wallet": 500, "drawer": 500, "bank": 500}, 
                         ignore_index=True)
moneyDB = moneyDB.append({"years": 2018, "months": 9, "days": 25, "wallet": 500, "drawer": 500, "bank": 500}, 
                         ignore_index=True)

today = date.today()


def addMoney(df):
    currentMoney = {"wallet": 0, "drawer": 0, "bank": 0}

    currentMoney["wallet"] = int(input("in the wallet: "))
    currentMoney["drawer"] = int(input("in the drawer: "))
    currentMoney["bank"] = int(input("in the bank account: "))

    matchingRows = df[(moneyDB["years"] == today.year) & (df["months"] == today.month) & (df["days"] == today.day)]

    if matchingRows.empty:
        df = df.append({"years": today.year, "months": today.month, "days": today.day,
                        "wallet": currentMoney["wallet"], "drawer": currentMoney["drawer"],
                        "bank": currentMoney["bank"]}, ignore_index=True)
    else:
        indexRow = matchingRows.iloc[0].name
        df = df.replace({"wallet": {df["wallet"][indexRow]: currentMoney["wallet"]},
                         "drawer": {df["drawer"][indexRow]: currentMoney["drawer"]},
                         "bank": {df["bank"][indexRow]: currentMoney["bank"]}})
    return df


def getSum(df):
    #df = df.sort_values(by=["years", "months", "days"], ascending=False).drop_duplicates(["months"], keep="first")
    print(df.head(100))
    lastMonth = df.iloc[0]
    lastMonthSum = int(lastMonth.wallet + lastMonth.drawer + lastMonth.bank)
    print(lastMonthSum)
    print("You have {} rubles in total".format(int(lastMonthSum)))
    return lastMonthSum

def compareMonths(df, lastMonthSum):
    if not df.iloc[1].empty:
        previousMonth = df.iloc[1]
        previousMonthSum = int(previousMonth.wallet + previousMonth.drawer + previousMonth.bank)

        if previousMonthSum > lastMonthSum:
            print("You have {} rubles less than last month.".format(previousMonthSum - lastMonthSum))
        elif previousMonthSum < lastMonthSum:
            print("Your current profit compared to last month is {} rubles.".format(
                lastMonthSum - previousMonthSum))
        else:
            "There is neither profit nor expenditure."

def getCleanedMoneyDB(moneyDB, cleanedMoneyDB):
    years = moneyDB.sort_values(by=["years"], ascending=False).drop_duplicates(["years"], keep="first")[
        "years"].tolist()
    #print(df.head(100))
    for year in years:
        #print(year)
        oneYear = moneyDB.loc[moneyDB["years"] == year].sort_values(by=["months", "days"], ascending=False) \
            .drop_duplicates(["months"], keep="first")
        cleanedMoneyDB = pd.concat([cleanedMoneyDB, oneYear], ignore_index=True)
        #print(oneYear)
    return cleanedMoneyDB

def getExpenditure(df):
    pass


def getProfit(df):
    pass

def showListByMonths(df, n = 10):
    return df.head(n)

while input("Would you lile to add an entry (y/n)? ") == "y":
    #clear_output()
    moneyDB = addMoney(moneyDB)
    print(moneyDB)

cleanedMoneyDB = getCleanedMoneyDB(moneyDB, cleanedMoneyDB)
if input("Would you lile to know the amount of money you currently have(y/n)? ") == "y":
    sum = getSum(cleanedMoneyDB)
    compareMonths(moneyDB, sum)

if input("Do you want to see the list of entries (y/n)? ") == "y":
    print(showListByMonths(cleanedMoneyDB, input("How many entries do you want to get at once (number)?")))