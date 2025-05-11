import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_athletes_with_the_most_appearances_at_Olympic_Games#Dual_sport_and_multi-sport_Olympians'
tables = pd.read_html(url)
df = tables[2]
print(df)
print(df.columns)

df.columns.values[7] = 'Gold'
df.columns.values[8] = 'Silver'
df.columns.values[9] = 'Bronze'
df.columns.values[10] = 'Total'


print(df['Representing'])

df.to_csv('ucesnici_po_godinama_i_disciplinama.csv', index = False)