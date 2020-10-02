import pandas as pd
from datetime import date
from datetime import time
from random import randrange
#from IPython.display import clear_output

class personalFinance():
    def __init__(self):
        
        self.moneyDB = pd.DataFrame.from_dict({"years": [], "months": [], "days": [], "wallet": [], "drawer": [],
                                          "bank": []}).astype("int64")
        self.cleanedMoneyDB = self.moneyDB.copy()
        
        count = 0
        while count < 12:
            self.moneyDB = self.moneyDB.append({"years": randrange(2016, 2020), "months": randrange(1, 13), "days": randrange(1, 32),
                                      "wallet": randrange(0, 1000), "drawer": randrange(0, 1000), "bank": randrange(0, 1000)},
                                     ignore_index=True)
            count += 1
        
        self.today = date.today()
    
    
    def addMoney(self, df):
        currentMoney = {"wallet": 0, "drawer": 0, "bank": 0}
    
        num = input("in the wallet: ")
        currentMoney["wallet"] = num if num.isdigit() else 0
    
        num = input("in the drawer: ")
        currentMoney["drawer"] = num if num.isdigit() else 0
    
        num = input("in the bank account: ")
        currentMoney["bank"] = num if num.isdigit() else 0
    
        matchingRows = df[(self.moneyDB["years"] == self.today.year) & (df["months"] == self.today.month) & (df["days"] == self.today.day)]
    
        if matchingRows.empty:
            df = df.append({"years": self.today.year, "months": self.today.month, "days": self.today.day,
                            "wallet": currentMoney["wallet"], "drawer": currentMoney["drawer"],
                            "bank": currentMoney["bank"]}, ignore_index=True)
        else:
            indexRow = matchingRows.iloc[0].name
            df = df.replace({"wallet": {df["wallet"][indexRow]: currentMoney["wallet"]},
                             "drawer": {df["drawer"][indexRow]: currentMoney["drawer"]},
                             "bank": {df["bank"][indexRow]: currentMoney["bank"]}})
        return df
    
    
    def getSum(self, df):
        #df = df.sort_values(by=["years", "months", "days"], ascending=False).drop_duplicates(["months"], keep="first")
        #print(df.head(100))
        lastMonth = df.iloc[0]
        lastMonthSum = int(lastMonth.wallet + lastMonth.drawer + lastMonth.bank)
        print(lastMonthSum)
        print("You have {} rubles in total".format(int(lastMonthSum)))
        return lastMonthSum
    
    def compareMonths(self, df, lastMonthSum):
        if not df.iloc[1].empty:
            response = ""
            previousMonth = df.iloc[1]
            previousMonthSum = int(previousMonth.wallet + previousMonth.drawer + previousMonth.bank)
    
            if previousMonthSum > lastMonthSum:
                return "You have {} rubles less than last month.".format(previousMonthSum - lastMonthSum)
            elif previousMonthSum < lastMonthSum:
                return"Your current profit compared to last month is {} rubles.".format(
                    lastMonthSum - previousMonthSum)
            else:
                return "There is neither profit nor expenditure."

    # return dataframe that contains only the last day of a month and has no duplicates 
    def getCleanedMoneyDB(self, df, emptyDF):
        years = df.sort_values(by=["years"], ascending=False).drop_duplicates(["years"], keep="first")[
            "years"].tolist()
        #print(df.head(100))
        for year in years:
            #print(year)
            oneYear = df.loc[df["years"] == year].sort_values(by=["months", "days"], ascending=False) \
                .drop_duplicates(["months"], keep="first")
            emptyDF = pd.concat([emptyDF, oneYear], ignore_index=True)
            #print(oneYear)
        return emptyDF
    
    def getExpenditure(self):
        pass
    
    
    def getProfit(self):
        pass
    
    def saveMoneyDB(self):
        pass
    
    def loadMoneyDB(self):
        pass
    
    def showListByMonths(self, df, n):
        if n.isdigit():
            n = int(n)
        elif not n or not isinstance(n, int):
            n = 1000
        return df.head(n)

    def start(self):
        while input("Would you lile to add an entry (y/n)? ") == "y":
            #clear_output()
            self.moneyDB = self.addMoney(self.moneyDB)
            print(self.moneyDB)

        self.cleanedMoneyDB = self.getCleanedMoneyDB(self.moneyDB, self.cleanedMoneyDB)
        #print(self.cleanedMoneyDB.head(100))
        if input("Would you lile to know the amount of money you currently have(y/n)? ") == "y":
            sum = self.getSum(self.cleanedMoneyDB)
            print(self.compareMonths(self.moneyDB, sum))

        if input("Do you want to see the list of entries (y/n)? ") == "y":
            print(self.showListByMonths(self.cleanedMoneyDB, input("How many entries do you want to get at once (number)?")))

finance = personalFinance()
finance.start()