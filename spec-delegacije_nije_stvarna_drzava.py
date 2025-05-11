import pandas as pd
import re

url3='https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table#Special_delegations_with_medals'
tables3 = pd.read_html(url3)

df3 = tables3[4]
print(df3)

df3 = df3.reset_index()

df3.columns = df3.columns.droplevel(1)

df3.columns.values[0] = 'Index'
df3.columns.values[1] = 'Team'
df3.columns.values[2] = 'Num of summer games'
df3.columns.values[3] = 'Num of summer gold medals'
df3.columns.values[4] = 'Num of summer silver medals'
df3.columns.values[5] = 'Num of summer bronze medals'
df3.columns.values[6] = 'Total num of summer medals'

df3.columns.values[7] = 'Num of winter games'
df3.columns.values[8] = 'Num of winter gold medals'
df3.columns.values[9] = 'Num of winter silver medals'
df3.columns.values[10] = 'Num of winter bronze medals'
df3.columns.values[11] = 'Total num of winter medals'

df3.columns.values[12] = 'Combined total number of Games'
df3.columns.values[13] = 'Combined total number of gold medals'
df3.columns.values[14] = 'Combined total number of silver medals'
df3.columns.values[15] = 'Combined total number of bronze medals'
df3.columns.values[16] = 'Combined total number of all medals'

print(df3['Num of summer games'].head(50))
print(df3.isnull().sum())
df3 = df3.drop(10)
print(df3.columns)
print('')


df3["Team"] = df3["Team"].apply(lambda x: re.sub(r"\s*\(.*?\)|\s*\[.*?\]", "", x).strip())


# rucno_kontinenti = {
#     'Australasia': 'Oceania',
#     'Bohemia': 'Europe',
#     'British West Indies': 'North America',
#     'Czechoslovakia': 'Europe',
#     'United Team of Germany': 'Europe',
#     'East Germany': 'Europe',
#     'West Germany': 'Europe',
#     'Kosovo': 'Europe',
#     'Netherlands Antilles': 'North America',
#     'Russian Empire': 'Europe',
#     'Soviet Union': 'Europe',
#     'Serbia and Montenegro': 'Europe',
#     'Chinese Taipei': 'Asia',
#     'Virgin Islands': 'North America',
#     'Yugoslavia': 'Europe'
# }
# df3['Continent'] = None
#
# df3['Continent'] = df3['Continent'].fillna(df3['Team'].map(rucno_kontinenti))
# print(df3['Continent'].head(10))

continent_mapping = {
    'Australasia': 'Oceania',
    "Individual Neutral Athletes": "Neutral",
    "Refugee Olympic Team": "Neutral",
    "United Team of Germany": "Europe",
    "Unified Team": "Europe",
    "Olympic Athletes from Russia": "Europe",
    "ROC": "Europe",
    "Independent Olympic Athletes": "Neutral",
    "Independent Olympic Participants": "Neutral",
    "Mixed team": "Mixed"
}

df3['Continent'] = df3['Team'].map(continent_mapping)

# 1. Prikazi sve specijalne delegacije koje su
# ucestvovale samo na letnjim ili samo na zimskim igrama

# only_summer_or_winter = df3[
#     ((df3['Num of summer games'] > 0) & (df3['Num of winter games'] == 0)) |
#     ((df3['Num of summer games'] == 0) & (df3['Num of winter games'] > 0))
# ]

# print(only_summer_or_winter[['Team', 'Num of summer games', 'Num of winter games']])


# 2. Pronadji delegacije koje su ucestvovale samo jednom (bilo leto ili zima)

# just_once = df3[df3['Combined total number of Games'] == 1]
# print(just_once['Team'])
# print('')

# 3. Koja delegacija ima najveci prosek medalja po igri

# best_avg = df3['Combined total number of all medals'] / df3['Combined total number of Games']
# print(best_avg.sort_values(ascending=False))
# print('')
#
# # 4. Koja delegacija je imala vise uspeha na zimskim igrama nego na letnjim
#
# more_succ_in_winter_games = df3[df3['Num of winter gold medals'] > df3['Num of summer gold medals']]
# print(more_succ_in_winter_games['Team'])
# print('')
#
#
# # 5. Delegacije koje nikad nisu osvojile zlatnu medalju,
# # ali su osvojile bar neku srebrnu ili bronzanu
#
# no_gold = df3[
#     (df3['Combined total number of gold medals'] == 0) &
#     (df3['Combined total number of silver medals'] > 0) &
#     (df3['Combined total number of bronze medals'] > 0)]
#
# print(no_gold['Team'])
# print('')
#
# # 6. Koja delegacija ima najveci udeo bronzanih medalja u ukupnim medaljama
#
# most_bronze = (df3['Combined total number of bronze medals'] /
#                df3['Combined total number of all medals'])*100
#
# print('Most bronze:\n',df3.iloc[most_bronze.idxmax()]['Team'])
# print('')
#
# # 7. Prikazi koje delegacije su osvojile vise medalja nego
# # sto su ucestvovale na igrama
#
#
# more_medals_than_part = df3[df3['Combined total number of all medals'] > df3['Combined total number of Games']]
# print(more_medals_than_part['Team'])
# print('')
#
# # 8. Napravi rang listu delegacija po ukupnom broju osvojenih medalja.
#
# rank_list = df3.groupby('Team')['Combined total number of all medals'].sum().sort_values(ascending=False)
# print(rank_list)
# print('')
#
#
# # 9. Prikazi delegacije koje imaju ravnomerno rasporedjene medalje
#
# same_num_of_medals = df3[(df3['Combined total number of gold medals'] == df3['Combined total number of silver medals']) &
#                      (df3['Combined total number of silver medals'] == df3['Combined total number of bronze medals'])]
#
# print(same_num_of_medals['Team'])
# print('')
#
#
# # 10. Zemlje sa najmanje medalja u svim Olimpijadama
#
# min_num_of_medals = df3.sort_values(by='Combined total number of all medals', ascending=True)
# print(min_num_of_medals[['Team', 'Combined total number of all medals']])
# print('')
#
# # 11. Delegacije sa vecim brojem bronzanih nego zlatnih medalja
#
# more_bronze_than_gold= df3[df3['Combined total number of bronze medals'] > df3['Combined total number of gold medals']]
# print(more_bronze_than_gold[['Team','Combined total number of bronze medals', 'Combined total number of gold medals']])
# print('')
#
# # 12. Delegacije sa istim brojem zlatnih i srebrnih medalja
#
# same_num_of_gold_and_silver = df3[df3['Combined total number of gold medals'] == df3['Combined total number of silver medals']]
# print(same_num_of_gold_and_silver[['Team','Combined total number of gold medals','Combined total number of silver medals']])
# print('')
#
#
# # 13. Zemlje sa vise srebrnih nego bronzanih medalja
#
# more_silver_than_bronze = df3[df3['Combined total number of silver medals'] > df3['Combined total number of bronze medals']]
# print(more_silver_than_bronze[['Team','Combined total number of silver medals','Combined total number of bronze medals']])
#
# # 14. Delegacije sa najvise medalja u određenoj Olimpijadi (letnjoj ili zimskoj)
#
# most_num_of_summer_medals = df3.groupby('Team')['Total num of summer medals'].sum().sort_values(ascending=False)
# print(most_num_of_summer_medals)
# print('')
# most_num_of_winter_medals = df3.groupby('Team')['Total num of winter medals'].sum().sort_values(ascending=False)
# print(most_num_of_winter_medals)
# print('')

#
# # 15.  Zemlje koje pocinju sa slovo 'A' i imaju vise od 50 medalja
#
# countries_start_with_a = df3[(df3['Team'].str.startswith('A')) & (df3['Combined total number of all medals'] > 50)]
# print(countries_start_with_a[['Team','Combined total number of all medals']])
# print('')
#
# # 16. Zemlje koje sadrze slovo "n"
#
# countries_cont_n = df3[df3['Team'].str.contains('n',case=False)]
# print("Countries with 'n':\n",countries_cont_n['Team'])
# print('')
#
# # 17. Zemlje koje zavrsavaju sa "ia"
#
# countries_ends_with_ia = df3[df3['Team'].str.endswith('ia')]
# print(countries_ends_with_ia['Team'])
# print('')
#
# # 18. Zemlje koje sadrze rec "Republic"
#
# word_republic = df3[df3['Team'].str.contains('Republic',case=False)]
# print(word_republic['Team'])
# print('')
#
# # 19. Zemlje koje imaju broj medalja koji je deljiv sa 5
#
# num_div_with_5 = df3[df3['Combined total number of all medals'] % 5 == 0]
# print(num_div_with_5[['Team','Combined total number of all medals']])
#
#
# # 20. Dodaj novu kolonu u kojoj ce stajati
# # ocena uspeha zemlje na osnovu ukupnog broja medalja:
#
# # Ako ima vise od 100 medalja: "Veoma uspesna"
# # Ako ima izmedju 50 i 100 medalja: "Uspesna"
# # Ako ima manje od 50 medalja: "Manje uspesna"


# df3['Grade for success'] = df3.apply(lambda x: 'Veoma uspesna' if x['Combined total number of all medals'] > 100
#                                      else ('Uspesna' if x['Combined total number of all medals'] >= 50
#                                      else 'Manje uspesna'), axis =1)
#
# print(df3[['Team','Grade for success']])
# print('')

print(df3[['Team','Continent']])


df3.to_csv('spec_delegacije_nije_stvarna_drzava.csv', index = False)