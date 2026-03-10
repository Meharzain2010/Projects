import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df =  pd.read_csv("Resources/Sample - Superstore.csv",encoding = "latin1")
data = df.copy()


data.head()
data.info()
data.describe()

data.isnull().sum()
data.duplicated().sum()
data.drop_duplicates(inplace = True)

data["Order Date"] = pd.to_datetime(data["Order Date"])
data["Ship Date"] = pd.to_datetime(data["Ship Date"])


data.head()
data.duplicated().sum()

data["Order Month"] = data["Order Date"].dt.month

sales_by_category  = data.groupby("Category")["Sales"].sum().reset_index()
profit_by_category  = data.groupby("Category")["Profit"].sum().reset_index()


sales_by_month = data.groupby("Order Month")["Sales"].sum().reset_index()
profit_by_month = data.groupby("Order Month")["Profit"].sum().reset_index()
Months = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
sales_by_month["Month_Name"] = sales_by_month["Order Month"].map(Months)
profit_by_month["Month_Name"] = profit_by_month["Order Month"].map(Months)




plt.figure(figsize = (16,6))
plt.subplot(1,2,1)
sns.barplot(
    data = sales_by_category,
    x = "Category",
    y = "Sales",
    palette = "Blues_d")
plt.title("Sales_by_Category")
for i in range(len(sales_by_category["Category"])):
    plt.text(sales_by_category["Category"][i],sales_by_category["Sales"][i] + sales_by_category["Sales"][i] * 0.02,str(sales_by_category["Sales"][i].astype(int)),ha = "center")


plt.subplot(1,2,2)
sns.barplot(
    data = profit_by_category,
    x = "Category",
    y = "Profit",
    palette = "Greens_d"
)
plt.title("Profit_by_Category")

for i in range(len(profit_by_category["Category"])):
    plt.text(profit_by_category["Category"][i],profit_by_category["Profit"][i] +profit_by_category["Profit"][i] * 0.02,str(profit_by_category["Profit"][i].astype(int)),ha = "center")


plt.suptitle("Ecomerce Sales Vs Profit Analysis")
plt.tight_layout()
plt.show()




plt.figure(figsize = (16,6))
plt.subplot(1,2,1)
sns.lineplot(
    data = sales_by_month,
    x = "Month_Name",
    y = "Sales",
    color = "green",
    marker = "o"

)

plt.title("Sales_by_Month")
plt.xlabel("Months")
plt.grid()
for i in range(len(sales_by_month["Month_Name"])):
    plt.text(sales_by_month["Month_Name"][i],sales_by_month["Sales"][i]+sales_by_month["Sales"][i]*0.05,str(sales_by_month["Sales"][i].astype(int)),ha = "center")
plt.tight_layout()
plt.ylim(min(sales_by_month["Sales"])-2000,max(sales_by_month["Sales"])+30000)



plt.subplot(1,2,2)
sns.lineplot(
    data = profit_by_month,
    x = "Month_Name",
    y = "Profit",
    color = "green",
    marker = "o"
)
plt.title("Profit_by_Month")
plt.xlabel("Months")

plt.suptitle("Monthly Sales Vs Profit Analysis")
plt.grid()
for i in range(len(profit_by_month["Month_Name"])):
    plt.text(profit_by_month["Month_Name"][i],profit_by_month["Profit"][i] + profit_by_month["Profit"][i] * 0.05 ,str(profit_by_month["Profit"][i].astype(int)),ha = "center")
plt.tight_layout()
plt.ylim(min(profit_by_month["Profit"])-2000,max(profit_by_month["Profit"])+5000)

plt.show()
