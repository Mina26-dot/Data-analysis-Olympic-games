import pandas as pd
import matplotlib.pyplot as plt

url = 'https://www.olympedia.org/sports'
tables = pd.read_html(url)
df = tables[0]
print(df)
print(df.columns)
unique_sports = df['Sport'].unique()
print(unique_sports)
print(df.columns)




