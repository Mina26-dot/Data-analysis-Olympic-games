import pandas as pd

url11 = 'https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table#Combined_total_(1896%E2%80%932024)'
tables11 = pd.read_html(url11)
df11 = tables11[16]

df11 = df11.reset_index(drop = True)
print(df11)

print(df11.columns)
print(df11.isnull().sum())
print(df11.describe())
print(df11.duplicated())

# 1. Sortiraj tabelu po broju osvojenih zlatnih medalja (Gold) opadajuce

sorted_df = df11.sort_values(by='Gold', ascending=False)
print(sorted_df)
print('')

# 2. Pronadji zemlju (NOC) sa najvise osvojenih medalja ukupno.

top_country = df11.sort_values(by='Total', ascending=False).iloc[0]
print(top_country)
print('')


# 3. Izdvoj top 10 zemalja po ukupnom broju medalja

top_ten = df11.groupby('NOC')['Total'].sum().sort_values(ascending = False).head(10)
print(top_ten)
print('')


# 4. Pronadji prosecan broj medalja po zemlji

avg = df11.groupby('NOC')['Total'].mean()
print(avg)
print('')


# 5. Dodaj kolonu "Gold %" – procenat zlatnih medalja u odnosu na ukupne

df11['Gold %'] = round((df11['Gold']/df11['Total'])*100,2)
print(df11['Gold %'])
print('')


# 6. Prikazi zemlje koje imaju vise od 50% zlatnih medalja u odnosu na ukupno


more_than_50_perc_gold = df11[df11['Gold %'] > 50]
print(more_than_50_perc_gold)
print('')

# 7. Prikazi sve zemlje koje imaju vise srebrnih medalja nego zlatnih

more_silver_than_gold = df11[df11['Silver'] > df11['Gold']]
print(more_silver_than_gold[['NOC','Silver','Gold']])
print('')


# 8. Prikazi sve zemlje koje imaju jednak broj zlatnih i bronzanih medalja

equal_gold_and_bronze = df11[df11['Gold'] == df11['Bronze']]
print(equal_gold_and_bronze[['NOC','Gold','Bronze']])
print('')



# 9. Napravi rang listu baziranu na poenima umesto samo zlatu
# Umesto da rangiras zemlje samo po broju zlatnih medalja, napravi poene po sistemu:

# - 3 poena za zlato
# - 2 poena za srebro
# - 1 poen za bronzu

df11['Points'] = df11['Gold']*3 + df11['Silver']*2 + df11['Bronze']*1
rank_list = df11.sort_values(by='Points', ascending=False)
print(rank_list[['NOC', 'Gold', 'Silver', 'Bronze', 'Points']])
print('')

# 10. Pronadji zemlje koje su usle u top 10 po broju medalja, ali nisu medju top 10 po zlatu

top_10_total = df11.sort_values(by='Total', ascending=False).head(10)
top_10_gold = df11.sort_values(by='Gold', ascending=False).head(10)

top_10_total_nocs = set(top_10_total['NOC'])
top_10_gold_nocs = set(top_10_gold['NOC'])

difference = top_10_total_nocs - top_10_gold_nocs

result = df11[df11['NOC'].isin(difference)]
print(result[['NOC', 'Gold', 'Total']])
print('')


# 11. Izdvoj top 3 zemlje sa najvise srebrnih medalja


top_3_silver = df11.sort_values(by='Silver', ascending=False).head(3)
print(top_3_silver[['NOC', 'Silver']])
print('')


# 12. Pronadji razliku u broju medalja izmedju zlatnih i bronzanih za svaku zemlju


div = df11['Gold'] - df11['Bronze']
print(div)
print('')



# 13. Filtriraj zemlje sa vise od 10 zlatnih medalja i vise od 30 ukupnih medalja


result = df11[(df11['Gold'] > 10) & (df11['Total'] > 30)]
print(result[['NOC','Gold','Total']])
print('')

# 14. Izdvoj zemlje koje nisu osvojile ni zlatnu, ni srebrnu medalju.

zero_gold_and_silver = df11[(df11['Gold'] == 0) & (df11['Silver'] == 0)]
print(zero_gold_and_silver[['NOC','Gold','Silver']])
print('')


# 15. Prikazi zemlje koje su osvojile vise bronzanih medalja nego srebrnih


more_bronze_than_silver = df11[df11['Bronze'] > df11['Silver']]
print(more_bronze_than_silver[['NOC','Bronze','Silver']])
print('')


# 16. Prikazi zemlje koje su osvojile samo bronzane medalje


only_bronze = df11[(df11['Gold'] == 0) & (df11['Silver'] == 0) & (df11['Bronze'] > 0)]
print(only_bronze[['NOC','Gold','Silver','Bronze']])
print('')



# 17. Prikazi zemlje koje nemaju nijednu medalju

zero_medals = df11[df11['Total'] == 0]
print(zero_medals)
print('')


# 18. Prikazi sve zemlje koje imaju isti broj zlatnih i srebrnih medalja

equal_num_of_medals = df11[(df11['Gold'] == df11['Silver']) & (df11['Gold'] == df11['Bronze'])]
print(equal_num_of_medals[['NOC','Gold','Silver','Bronze']])
print('')

# 19. Prikazi top 5 zemalja po procentu zlatnih medalja u odnosu na ukupne

# perc_of_gold = round((df11['Gold'] / df11['Total'])*100,2)
# top_5_countries = perc_of_gold.sort_values(ascending=False).head(5)
# print(top_5_countries)

perc_of_gold_top_5 = df11.groupby('NOC')['Gold %'].sum().sort_values(ascending=False)
print(perc_of_gold_top_5.head(5))
print('')

# 20. Pronadji koliko zemalja ima tacno 0 zlatnih medalja


zero_gold = df11[df11['Gold'] == 0]
print(zero_gold[['NOC','Gold']])
print('')


# 21. Prikazi zemlje koje imaju broj medalja izmedju 10 i 20 (ukupno)

between_10_and_20_medals = df11[(df11['Total'] >= 10) & (df11['Total'] <= 20)]
print(between_10_and_20_medals[['NOC','Total']])
print('')

# 22. Pronadji prosecan broj zlatnih medalja po zemlji


avg_num_of_gold_per_country = df11.groupby('NOC')['Gold'].mean()
print(avg_num_of_gold_per_country)
print('')



df11.to_csv('kompletno_rangiranje_svih_medalja_bez_prethodnika.csv', index = False)
