import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests 
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
response = requests.get(URL)
if response.status_code == 200:
    print("It is Good to Go!")
else:
    print("Have Error..!",response)



with open(f"scrapped/data.html","w",encoding = "utf-8") as f:
    f.write(response.text)

with open(f"scrapped/data.html","r",encoding = "utf-8") as f:
    data = f.read()

soup = BeautifulSoup(data,"lxml")
jobs = soup.find_all("div",class_ = "card-content")
# print(jobs)

Jobs = []
Companies = []
Countries = []
Dates = []

for job in jobs:
    Job = job.find("h2",class_= "title is-5").text.strip()
    Company = job.find("h3",class_ = "subtitle is-6 company").text.strip()
    Country = job.find("p",class_ = "location").text.strip()
    Date = job.find("time").text.strip()


    Jobs.append(Job)
    Companies.append(Company)
    Countries.append(Country)
    Dates.append(Date)

new_data = pd.DataFrame({"Jobs":Jobs,"Company":Companies,"Country":Countries,"Date":Dates})   
new_data.to_csv("Jobs_data.csv",index = False)



df = pd.read_csv("Jobs_data.csv")



data_df = df.copy()

data_df.isnull().sum()
data_df.duplicated().sum()

data_df.dropna(inplace = True)
data_df.drop_duplicates(inplace = True)


employee_data = {}

roles = ["developer","engineer","manager","trader","officer","designer"]

for role in roles:
    employee_data[role.capitalize()] = data_df["Jobs"].str.contains(role,case= False).sum()


employees = pd.DataFrame(list(employee_data.items()),columns = ["Job","Count"])






Top_Jobs = data_df["Jobs"].value_counts().head(10).reset_index()
Top_Companies = data_df["Company"].value_counts().head(10).reset_index()



Top_Companies.columns = ["Company","Hiring Ratio"]
Top_Jobs.columns = ["Jobs","Demands"]






fig,ax = plt.subplots(figsize = (28,8))
sns.barplot(
    data = Top_Jobs,
    x = "Jobs",
    y="Demands",
    hue = "Demands",
    palette = "Reds_d",
    ax = ax
)
fig.suptitle("Jobs Vs Company Hiring")


for i in range(len(Top_Jobs)):
    plt.text(Top_Jobs["Jobs"][i],Top_Jobs["Demands"][i]+0.02,Top_Jobs["Demands"][i],ha = "center")
fig.tight_layout()
plt.savefig("Figures/1.Jobs Vs Company Hiring.png")
plt.show()



fig,ax = plt.subplots(figsize = (25,8))
sns.barplot(
    data = Top_Companies,
    x = "Company",
    y="Hiring Ratio",
    hue = "Hiring Ratio",
    palette = "Oranges_d",
    ax = ax
)
ax.set_title("Top Companies Hiring Ratio")


for i in range(len(Top_Companies)):
    plt.text(Top_Companies["Company"][i],Top_Companies["Hiring Ratio"][i]+0.02,Top_Companies["Hiring Ratio"][i],ha = "center")
fig.tight_layout()
plt.savefig("Figures/2.Top Companies Hiring Ratio.png")
plt.show()

fig,ax = plt.subplots(figsize = (25,8))
sns.lineplot(
    data = employees,
    x = "Job",
    y="Count",
    marker = "o",
    color = "green",
    ax = ax
)
ax.set_title("Number of Employees in Companies")

for i in range(len(employees)):
    ax.text(employees["Job"][i],employees["Count"][i]+employees["Count"][i] * 0.01,employees["Count"][i],ha = "center")
fig.tight_layout()
plt.savefig("Figures/3.Number of Employees in Companies.png")
plt.show()

fig,ax = plt.subplots(figsize = (12,8))
explode = [0,0.1,0,0,0,0]
plt.pie(
    employees["Count"],
    labels = employees["Job"],
    autopct = "%1.1f%%",
    explode  = explode,
    startangle  = 100,
    
    wedgeprops = {"edgecolor":"black",
                 "linestyle" : "--"}
)
plt.axis("equal") 
plt.title("Categories of Employee in Companies ")
plt.tight_layout()
plt.savefig("Figures/4.Categories of Employee in Companies.png")
plt.show()
