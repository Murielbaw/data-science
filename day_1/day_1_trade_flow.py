import pandas as pd

# read the CSV file with utf-8 encoding
df = pd.read_csv('day_1\RFM_TRAD_FLOW.csv', encoding='gbk')

F = df.groupby(['cumid','type'])['transID'].count()

# print the first few rows of the dataframe
print(F.head())





