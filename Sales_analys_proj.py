import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

#Merging 12 months of sales data into single file
os.chdir(r"C:\Users\Konrad\Documents\GitHub\Python\udemy\data science")

df=pd.read_csv(r'./Sales_Data/Sales_April_2019.csv')

files=[file for file in os.listdir(r'./Sales_Data')]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv(r'./Sales_Data/'+file)
    all_months_data=pd.concat([all_months_data, df])

all_months_data.to_csv('all_data.csv', index=False)
#Read updated dataframe
all_data=pd.read_csv('all_data.csv')

#Clean the data
nan_df = all_data[all_data.isna().any(axis=1)]

all_data = all_data.dropna(how='any')

all_data = temp_df = all_data[all_data['Order Date'].str[0:2]!='Or']

all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

#Augmented data with additional columns
#Task 2: Add month column

all_data['Month']=all_data['Order Date'].str[0:2]
all_data['Month']=all_data['Month'].astype('int32')

#Task 3: Add sales column

all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

#Task 4: Add city column
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split()[0]

all_data['Cities'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")


#Q1: What was the best month for sales? How much was earned that month?
# resultsQ1=all_data.groupby('Month').sum()

# months = range(1,13)

# plt.bar(months, resultsQ1['Sales'])
# plt.xticks(months)
# plt.ylabel('Sales in USD')
# plt.xlabel('Month number')
# plt.show()

#Q2: What city had the highest number of sales
city_citizens={'Atlanta (GA)': 497642,'Austin (TX)': 965872, 'Boston (MA)': 689326,'Dallas (TX)': 1339000,'Los Angeles (CA)': 3973000,'New York City (NY)': 8380000,'Portland (OR)': 650390,'San Francisco (CA)': 874784, 'Seattle (WA)': 741251}

city_citizens=[497642, 965872, 689326, 1339000, 3973000, 8380000, 650390, 874784, 741251]
resultsQ2=all_data.groupby('Cities').sum()

# for index, value in enumerate(city_citizens):
#     resultsQ2['Sales'].apply(resultsQ2['Sales'][index]/value)
# print(resultsQ2)

# cities = all_data['Cities'].unique()
# cities = [city for city, df in all_data.groupby('Cities')]

# plt.bar(cities, resultsQ2['Sales'])
# plt.xticks(cities, rotation='vertical', size=6)
# plt.ylabel('Sales in USD')
# plt.xlabel('City name')
# plt.show()

#print(all_data.head())

#Q3 What thime should we display advertisments to maximize lielihood of customers buying product?
# all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])

# all_data['Hour']=all_data['Order Date'].dt.hour
# all_data['Minute']=all_data['Order Date'].dt.minute

# hours = [hour for hour, df in all_data.groupby('Hour')]

# plt.plot(hours, all_data.groupby(['Hour']).count())
# plt.xticks(hours)
# plt.grid()
# plt.ylabel('Number of Orders')
# plt.xlabel('Hours')
# plt.show()

#Q4 What products are most often sold together?
df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df=df[['Order ID', 'Grouped']].drop_duplicates()

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key, value in count.most_common(10):
    print(key, value)

#Q5 What products sell the most
product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

products = [product for product, df in product_group]

plt.bar(products, quantity_ordered)
plt.xticks(products, rotation='vertical', size=6)
plt.ylabel('Sales in qty')
plt.xlabel('Product name')
plt.show()

prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered)
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)
plt.show()