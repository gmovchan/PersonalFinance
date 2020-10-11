import pandas as pd
from datetime import date
from datetime import time
from random import randrange
from sqlalchemy import create_engine
#from IPython.display import clear_output


#print(engine.table_names())

#table = engine.execute("SELECT * FROM money")
#print(table.keys())
#print(table.column_descriptions())

'''def createNewEngine():
    moneyDB = pd.DataFrame.from_dict({"users": [], "years": [], "months": [], "days": [], "wallet": [], "drawer": [],
                                      "bank": []}).astype("int64")

    for x in range(12):
        moneyDB = moneyDB.append({"users": randrange(183291591, 183291594), "years": randrange(2016, 2020), "months":
            randrange(1, 13), "days": randrange(1, 32), "wallet": randrange(0, 1000), "drawer": randrange(0, 1000),
                                  "bank":
                                      randrange(0, 1000)}, ignore_index=True)

    engine = create_engine("sqlite://", echo=False)
    moneyDB.to_sql("money", con=engine)
    return engine'''

engine = create_engine("sqlite:///C:\\sqlite\\finance.db", echo=False)



class personalFinance():
    def __init__(self, engine, user_id):
        
        '''self.moneyDB = pd.DataFrame.from_dict({"users": [], "years": [], "months": [], "days": [], "wallet": [], "drawer": [],
                                          "bank": []}).astype("int64")

        self.emptyMoneyDB = self.moneyDB.copy()

        for x in range(12):
            self.moneyDB = self.moneyDB.append({"years": randrange(2016, 2020), "months": randrange(1, 13), "days": randrange(1, 32),
                                      "wallet": randrange(0, 1000), "drawer": randrange(0, 1000), "bank": randrange(0, 1000)},
                                     ignore_index=True)'''

        self.user = user_id
        self.engine = engine
        query = "SELECT * FROM money WHERE users = {}".format(user_id)
        self.moneyDB = pd.read_sql_table("money", self.engine, index_col="index")
        self.moneyDB = self.moneyDB[self.moneyDB["users"] == int(user_id)]

        print(self.moneyDB)

        self.emptyMoneyDB = self.moneyDB[0:0].copy()
        
        self.today = date.today()

        self.cleanedTable = self.updateCleanedTable()

    def saveToSQL(self):
        self.moneyDB.to_sql("money", self.engine, if_exists="replace", index_label="index")
        print(self.engine.execute("SELECT * FROM money").fetchall())
    
    
    def addMoney(self, pockets):

        for key in pockets:
            print(key)
            pockets[key] = int(pockets[key])

        df = self.moneyDB
        # check whether you have already added money today or not. If you have done it then the last entry
        # will be rewritten.
        matchingRows = df[(self.moneyDB["years"] == self.today.year) & (df["months"] == self.today.month) & (df["days"] == self.today.day)]
    
        if matchingRows.empty:
            df = df.append({"users": self.user, "years": self.today.year, "months": self.today.month, "days": self.today.day,
                            "wallet": pockets["wallet"], "drawer": pockets["drawer"],
                            "bank": pockets["bank"]}, ignore_index=True)
        else:
            indexRow = matchingRows.iloc[0].name
            df = df.replace({"wallet": {df["wallet"][indexRow]: pockets["wallet"]},
                             "drawer": {df["drawer"][indexRow]: pockets["drawer"]},
                             "bank": {df["bank"][indexRow]: pockets["bank"]}})
        self.moneyDB = df
        self.saveToSQL()

    def getLastMonth(self):
        self.updateCleanedTable()
        lastMonth = self.cleanedTable.iloc[0]
        return lastMonth
    
    
    def getSum(self):
        lastMonth = self.getLastMonth()
        lastMonthSum = int(lastMonth.wallet + lastMonth.drawer + lastMonth.bank)
        #print(lastMonthSum)
        #print("You have {} rubles in total".format(int(lastMonthSum)))
        return lastMonthSum

    def getPockets(self):
        lastMonth = self.getLastMonth()
        pockets = {"wallet": lastMonth.wallet, "drawer": lastMonth.drawer, "bank": lastMonth.bank}
        return pockets

    # it throws an error if self.cleanedTable has only one row
    def compareMonths(self):

        currentMonthSum = self.getSum()

        message = "You've saved up {} rubles.".format(currentMonthSum)

        if not self.cleanedTable.iloc[1].empty:
            response = ""
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
        #print(self.moneyDB)
        cleandDF = self.emptyMoneyDB.copy()
        years = self.moneyDB.sort_values(by=["years"], ascending=False).drop_duplicates(["years"], keep="first")[
            "years"].tolist()
        #print(years)
        for year in years:
            #print(year)
            oneYear = self.moneyDB.loc[self.moneyDB["years"] == year].sort_values(by=["months", "days"], ascending=False) \
                .drop_duplicates(["months"], keep="first")
            cleandDF = pd.concat([cleandDF, oneYear], ignore_index=True)
            #print(oneYear)
        #print(cleandDF)
        self.cleanedTable = cleandDF
        return True
    
    def getExpenditure(self):
        pass
    
    
    def getProfit(self):
        pass
    
    def saveMoneyDB(self):
        pass
    
    def loadMoneyDB(self):
        pass
    
    def showListByMonths(self):
        '''if n.isdigit():
            n = int(n)
        elif not n or not isinstance(n, int):
            n = 1000'''
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

        # clear_output()
        self.addMoney(pockets)
        print(self.moneyDB)

    def getJSON(self):
        self.updateCleanedTable()
        return self.cleanedTable.to_json()

    def getTable(self):
        self.updateCleanedTable()
        #print(self.cleanedTable.to_string())
        #return "<pre>" + self.cleanedTable.to_string() + "</pre>"
        #return self.cleanedTable.to_string()

        print(self.cleanedTable.to_string())

        result = ""

        for index, row in self.cleanedTable.iterrows():
            sum = int(row['wallet']) + int(row['drawer']) + int(row['bank'])
            result += "Date: {}/{}/{}\nwallet {} \u20BD, drawer {} \u20BD, bank {} \u20BD\nIn total: {} \u20BD\n\n".format(row['days'], row['months'], \
            row['years'], row['wallet'], row['drawer'], row['bank'], sum)

        print(result)

        return result

    def start(self):
        while input("Would you like to add an entry (y/n)? ") == "y":
            self.inputMoneyToAdd()
        #print(self.cleanedTable.head(100))
        if input("Would you like to know the amount of money you currently have(y/n)? ") == "y":
            print(self.compareMonths())

        if input("Do you want to see the list of entries (y/n)? ") == "y":
            print(self.showListByMonths())

#finance = personalFinance(engine)
#print(finance.getJSON())
#finance.start()
#print(finance.getTable())