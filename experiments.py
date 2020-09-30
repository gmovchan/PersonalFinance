import pandas as pd

moneyDB = pd.DataFrame.from_dict({"years": [], "months": [], "days": [], "wallet": [], "drawer": [],
                                  "bank": []}).astype("int64")

moneyDBByYears = moneyDB.copy()

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

#print(moneyDB.sort_values(by=["years", "months", "days"], ascending=False).groupby("months").head(100))
#print(moneyDB.sort_values(by=["years", "months", "days"], ascending=False).duplicated(["months"], keep="first").head(100))
#print(moneyDB[moneyDB.sort_values(by=["years", "months", "days"], ascending=False).duplicated(["months"], keep="last").head(100)])
#print(moneyDB.sort_values(by=["years", "months", "days"], ascending=False).drop_duplicates(["months"], keep="first").head(100))
#print(moneyDB.sort_values(by=["years"], ascending=False).drop_duplicates(["years"], keep="first")["years"].tolist())

years = moneyDB.sort_values(by=["years"], ascending=False).drop_duplicates(["years"], keep="first")["years"].tolist()
print(moneyDB.head(100))
for year in years:
    print(year)
    oneYear = moneyDB.loc[moneyDB["years"] == year].sort_values(by=["months", "days"], ascending=False)\
        .drop_duplicates(["months"], keep="first")
    moneyDBByYears = pd.concat([moneyDBByYears, oneYear], ignore_index=True)
    print(oneYear)

print(moneyDBByYears.head(100))
#print(moneyDB["years"].tolist())