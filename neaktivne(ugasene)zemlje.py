import pandas as pd
import pycountry
import pycountry_convert as pc
import re

url2='https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table#List_of_defunct_historical_NOCs_and_special_delegations_with_medals_(sortable_&_unranked)'
tables2 = pd.read_html(url2)

df2 = tables2[3]
# print(df2)

df2 = df2.reset_index()

df2.columns = df2.columns.droplevel(1)

df2.columns.values[0] = 'Index'
df2.columns.values[1] = 'Team'
df2.columns.values[2] = 'Num of summer games'
df2.columns.values[3] = 'Num of summer gold medals'
df2.columns.values[4] = 'Num of summer silver medals'
df2.columns.values[5] = 'Num of summer bronze medals'
df2.columns.values[6] = 'Total num of summer medals'

df2.columns.values[7] = 'Num of winter games'
df2.columns.values[8] = 'Num of winter gold medals'
df2.columns.values[9] = 'Num of winter silver medals'
df2.columns.values[10] = 'Num of winter bronze medals'
df2.columns.values[11] = 'Total num of winter medals'

df2.columns.values[12] = 'Combined total number of Games'
df2.columns.values[13] = 'Combined total number of gold medals'
df2.columns.values[14] = 'Combined total number of silver medals'
df2.columns.values[15] = 'Combined total number of bronze medals'
df2.columns.values[16] = 'Combined total number of all medals'

print(df2.head(50))
print(df2.columns)
print(df2.describe())
print(df2['Team'].nunique())
print(df2.isnull().sum())
df2 = df2.drop(10)


df2['Team'] = df2['Team'].apply(lambda x: re.sub(r"(\s*\[.*?\]|\s*\(.*?\))+", "", x).strip())


# 1. Prikazi hronoloski koje ugasene zemlje su ucestvovale
# na najvise Olimpijskih igara

# countries = df2.groupby('Team')['Combined total number of Games'].sum().sort_values(ascending=False)
# print(countries)


# 2. Pronadji ugasene zemlje koje su osvajale
# medalje samo na letnjim ili samo na zimskim igrama

only_summer_or_winter = ((df2['Total num of summer medals'] > 0) ^ (df2['Total num of winter medals'] > 0))
print(df2[only_summer_or_winter])

# 3. Izdvoj ugasene zemlje koje su osvojile vise od 300 medalja ukupno.

countries_with_more_than_300 = df2[df2['Combined total number of all medals'] > 300]
print(countries_with_more_than_300)

# 4. Izdvoj zemlje koje su ucestvovale na manje od 5 igara,
# ali su osvojile bar 50 medalja.

countries = df2[(df2['Combined total number of Games'] < 5) & (df2['Combined total number of all medals'] >= 50)]
print(countries)


# 5. Pronadji ugasenu zemlju koja ima najvisi procenat
# zlatnih medalja u odnosu na ukupan broj medalja

percent_of_gold_medals = (df2['Combined total number of gold medals']/df2['Combined total number of all medals'])*100
print(percent_of_gold_medals)
print('')

# 6. Izdvoj zemlje koje su bile uspesnije na zimskim nego na letnjim igrama.

suc_winter = df2[(df2['Num of winter gold medals']) > (df2['Num of summer gold medals'])]
print(suc_winter['Team'])
print('')



# 7. Pronadji zemlje koje imaju vise bronzanih nego zlatnih i srebrnih zajedno.

more_bronze_than_gold_and_silver = df2[(df2['Combined total number of bronze medals'] > df2['Combined total number of gold medals']) & (df2['Combined total number of bronze medals'] > df2['Combined total number of silver medals'])]
print(more_bronze_than_gold_and_silver['Team'])
print('')


# 8. Prikazi razliku u ukupnim medaljama izmedju dve najuspesnije ugasene zemlje.

sorted_medals = df2.sort_values(by='Combined total number of all medals', ascending=False)

first_place = sorted_medals.iloc[0]['Combined total number of all medals']
second_place = sorted_medals.iloc[1]['Combined total number of all medals']

difference = first_place - second_place

print(f"Difference : {difference}")



# 9. Izdvoj zemlje sa najvecim prosekom medalja po Olimpijadi (kombinovano).


medals_per_game = df2['Combined total number of all medals'] / df2['Combined total number of Games']
avg = medals_per_game.sort_values(ascending=False)

print(avg)
print('')


# 10. Napravi boolean kolonu: Is_summer_stronger, koja pokazuje da li je tim osvojio vise medalja leti nego zimi.

df2['Is_summer_stronger'] = df2['Total num of summer medals'] > df2['Total num of winter medals']
print(df2['Is_summer_stronger'])
print('')

# 11. Kreiraj kolonu za ukupan broj medalja po igri

df2['Total_num_of_medals_per_game'] = round(df2['Combined total number of all medals'] / df2['Combined total number of Games'],2)
print(df2['Total_num_of_medals_per_game'])
print('')

# 12. Pronađi sve timove koji imaju bar jedno od slova 'x', 'q' ili 'z' u imenu

char = df2['Team'].str.contains(r'[xqz]', case=False)
print(char)


# 13. Filtriraj timove cije ime:

# - pocinje sa "A"
# - sadrzi tacno dve reci


starts_with_a = df2['Team'].str.startswith('A')
print(starts_with_a)
print('')

contains_two_words = df2['Team'].apply(lambda x : len(x.split()) == 2)
print(contains_two_words)
print('')


# 14. Dodaj kolonu has_a, koja kaže da li ime tima sadrzi slovo 'a' (True/False), koristeci apply i lambda

df2['has_a'] = df2['Team'].apply(lambda x: 'a' in x.lower())
print(df2['has_a'])
print('')

# 15. Filtriraj sve timove koji imaju više od 5 slova u imenu

filter = df2['Team'].apply(lambda x : True if len(x) > 5 else False)
print('Countries with more than 5 characters: \n',df2[filter]['Team'])
print('')

# 16. Pronadji sve timove koji pocinju sa "C"

start_with_c = df2['Team'].str.startswith('C')
print("Countries starts with 'C': \n",df2[start_with_c]['Team'])
print('')


# 17. Pronadji timove gde je drugo slovo "a"

second_char = df2['Team'].apply(lambda x: x if len(x) > 1 and x[1].lower() == 'a' else 'no')
print(df2[second_char != 'no'])
print('')

# 18. Timovi koji imaju vise od 3 reci u imenu

more_than_3 = df2['Team'].apply(lambda x : len(x.split()) > 3)
print(df2[more_than_3]['Team'])
print('')

# 19. Filtriraj sve timove koji imaju više od 10 zlatnih medalja na letnjim igrama.

more_than_10 = df2[df2['Combined total number of gold medals'] > 10]
print(more_than_10[['Team','Combined total number of gold medals']])
print('')

# 20. Grupisi timove prema broju letnjih medalja i prikazi sumu medalja za svaki tim.

group = df2.groupby('Team')['Total num of summer medals'].sum()
print(group)
print('')

# 21. Sortiraj timove po broju zlatnih medalja na letnjim igrama, u opadajućem redosledu.

sort = df2.groupby('Team')['Total num of summer medals'].sum().sort_values(ascending = False)
print(sort)
print('')



# 22. Izracunaj osnovnu statistiku (prosecno, maksimalno, minimalno, itd.) za broj zlatnih medalja na letnjim igrama.

avg = df2.groupby('Team')['Total num of summer medals'].mean()
print(avg)
print('')

max = df2.groupby('Team')['Total num of summer medals'].max()
print(max)
print('')

min = df2.groupby('Team')['Total num of summer medals'].min()
print(min)
print('')



df2.to_csv('neaktivne(ugasene)zemlje.csv', index = False)

