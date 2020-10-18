import pandas as pd
from datetime import date
#from datetime import time
from random import randrange
from sqlalchemy import create_engine

engine = create_engine("sqlite:///finance.db", echo=False)
#engine = create_engine("sqlite:///C:\\sqlite\\finance.db", echo=False)


class personalFinance():
    def __init__(self, engine, user_id):

        self.user = user_id
        self.engine = engine
        self.moneyDB = False
        self.maxIndex = False
        self.emptyMoneyDB = False
        self.readSQL()
        self.today = date.today()
        self.cleanedTable = self.updateCleanedTable()

    def readSQL(self):
        self.moneyDB = pd.read_sql_table("money", self.engine, index_col="index")
        self.maxIndex = self.moneyDB.index.max()
        self.emptyMoneyDB = self.moneyDB[0:0].copy()

    def saveToSQL(self):
        self.moneyDB.to_sql("money", self.engine, if_exists="replace", index_label="index")

    def getNameOfMonth(self, n):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        monthDic = {}
        c = 0
        for x in range(1, 13):
            monthDic[x] = months[c]
            c += 1

        return monthDic[n]

    def addMoney(self, pockets):

        for key in pockets:
            pockets[key] = int(pockets[key])

        # check whether you have already added money today or not. If you have done it then the last entry
        # will be rewritten.
        matchingRows = self.moneyDB[(self.moneyDB["users"] == self.user) & (self.moneyDB["years"] == self.today.year) &
                                    (self.moneyDB["months"] == self.today.month) &
                                    (self.moneyDB["days"] == self.today.day)]

        if matchingRows.empty:
            '''self.moneyDB = self.moneyDB.append({"users": self.user, "years": self.today.year, "months": self.today.month, "days": self.today.day,
                            "wallet": pockets["wallet"], "drawer": pockets["drawer"],
                            "bank": pockets["bank"]}, ignore_index=True)'''
            newRow = pd.DataFrame.from_dict({"users": [self.user], "years": [self.today.year], "months": [self.today.month],
                                             "days": [self.today.day], "wallet": [pockets["wallet"]],
                                             "drawer": [pockets["drawer"]], "bank": [pockets["bank"]]}).astype("int64")

            self.maxIndex += 1
            newRow = newRow.rename(index={0: self.maxIndex})
            self.moneyDB = self.moneyDB.append(newRow)

        else:
            indexRow = matchingRows.iloc[0].name
            self.moneyDB = self.moneyDB.replace({"wallet": {self.moneyDB["wallet"][indexRow]: pockets["wallet"]},
                             "drawer": {self.moneyDB["drawer"][indexRow]: pockets["drawer"]},
                             "bank": {self.moneyDB["bank"][indexRow]: pockets["bank"]}})

        self.saveToSQL()

    def getLastMonth(self):
        self.updateCleanedTable()

        if len(self.cleanedTable.index.values) == 0:
            return self.emptyMoneyDB

        lastMonth = self.cleanedTable.iloc[0]
        return lastMonth
    
    
    def getSum(self):
        lastMonth = self.getLastMonth()
        if lastMonth.empty:
            return 0
        lastMonthSum = int(lastMonth.wallet + lastMonth.drawer + lastMonth.bank)
        return lastMonthSum

    def getPockets(self):
        lastMonth = self.getLastMonth()
        pockets = {"wallet": lastMonth.wallet, "drawer": lastMonth.drawer, "bank": lastMonth.bank}
        return pockets

    def compareMonths(self):

        currentMonthSum = self.getSum()

        message = "You've saved up {} rubles.".format(currentMonthSum)

        # check if the user has fewer than two months in the database
        if len(self.cleanedTable.index.values) > 1:
            previousMonth = self.cleanedTable.iloc[1]
            previousMonthSum = int(previousMonth.wallet + previousMonth.drawer + previousMonth.bank)

            message = "You've saved up {} rubles.".format(currentMonthSum)
    
            if previousMonthSum > currentMonthSum:
                message += "\nYou have {} rubles less than last month.".format(previousMonthSum - currentMonthSum)
            elif previousMonthSum < currentMonthSum:
                message += "\nYour current profit compared to last month is {} rubles.".format(
                    currentMonthSum - previousMonthSum)
            else:
                message += "\nThere is neither profit nor expenditure."

            return message
        else:
            message += "\nAnd this is your first month of tracking. Here is no other entries yet."
            return message

    # return dataframe that contains only the last day of a month and has no duplicates 
    def updateCleanedTable(self):
        cleandDF = self.emptyMoneyDB.copy()
        userMoneyDB = self.moneyDB[self.moneyDB["users"] == int(self.user)]
        years = userMoneyDB.sort_values(by=["years"], ascending=False).drop_duplicates(["years"], keep="first")[
            "years"].tolist()

        for year in years:
            oneYear = userMoneyDB.loc[userMoneyDB["years"] == year].sort_values(by=["months", "days"], ascending=False) \
                .drop_duplicates(["months"], keep="first")
            cleandDF = pd.concat([cleandDF, oneYear], ignore_index=True)

        self.cleanedTable = cleandDF
        return True
    
    def showListByMonths(self):
        self.updateCleanedTable()
        return self.cleanedTable.head(100)

    def inputMoneyToAdd(self):
        pockets = {"wallet": 0, "drawer": 0, "bank": 0}

        num = input("in the wallet: ")
        pockets["wallet"] = int(num) if num.isdigit() else 0

        num = input("in the drawer: ")
        pockets["drawer"] = int(num) if num.isdigit() else 0

        num = input("in the bank account: ")
        pockets["bank"] = int(num) if num.isdigit() else 0

        self.addMoney(pockets)

    def getJSON(self):
        self.updateCleanedTable()
        return self.cleanedTable.to_json()

    def getTable(self):
        self.updateCleanedTable()
        sortedDF = self.cleanedTable.copy()
        sortedDF = sortedDF.sort_values(by=["years", "months", "days"], ascending=True)

        result = ""

        for index, row in sortedDF.iterrows():
            sum = int(row['wallet']) + int(row['drawer']) + int(row['bank'])
            '''result += "Date: {}/{}/{}\nwallet {} \u20BD, drawer {} \u20BD, bank {} \u20BD\nIn total: {} \u20BD\n\n".format(row['days'], row['months'], \
            row['years'], row['wallet'], row['drawer'], row['bank'], sum)'''
            result += "{} {}\nwallet {} \u20BD, drawer {} \u20BD, bank {} \u20BD\nIn total: {} \u20BD\n\n".format(
                self.getNameOfMonth(row['months']), row['years'], row['wallet'], row['drawer'], row['bank'], sum)

        return result

    def fillDB(self, id):
        fakeDB = self.emptyMoneyDB.copy()

        for x in range(7):
            fakeDB = fakeDB.append({"users": id, "years": randrange(2016, 2020), "months": randrange(1, 13),
                                    "days": randrange(1, 32), "wallet": randrange(0, 1000), "drawer": randrange(0, 1000),
                                    "bank": randrange(0, 1000)}, ignore_index=True)

        fakeDB.to_sql("money", con=self.engine, if_exists="replace")

        return True

    def start(self):
        while input("Would you like to add an entry (y/n)? ") == "y":
            self.inputMoneyToAdd()

        if input("Would you like to know the amount of money you currently have(y/n)? ") == "y":
            print(self.compareMonths())

        if input("Do you want to see the list of entries (y/n)? ") == "y":
            print(self.showListByMonths())

if __name__ == "__main__":
    finance = personalFinance(engine, 100000000)