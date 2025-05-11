import pandas as pd
import pycountry
import pycountry_convert as pc

url1 = 'https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table#List_of_NOCs_without_medals_(sortable_&_unranked)'
tables1 = pd.read_html(url1)

df1 = tables1[2]
print(df1)

df1 = df1.reset_index()


df1.columns.values[1] = 'Team'
df1.columns.values[2] = 'Num of summer games'
df1.columns.values[3] = 'Num of winter games'
df1.columns.values[4] = 'Total num of all games'

# print(df1.columns)
# print(df1['Num of summer games'].dtype)
is_null = df1.isnull().sum()
print(is_null)
print(df1.duplicated())

print(df1['Total num of all games'])
print('')
df1['Clean Country'] = df1['Team'].str.split('(').str[0].str.strip()

def continent_of_country(country):
    try:
        code = pycountry.countries.lookup(country).alpha_2
        continent_code = pc.country_alpha2_to_continent_code(code)
        return pc.convert_continent_code_to_continent_name(continent_code)
    except:
        return 'Unknown'

df1['Continent'] = df1['Clean Country'].apply(continent_of_country)
print('Continent',df1['Continent'].head(50))
print('')
print(df1[['Team','Continent']].head(50))
print('')
#
# # 1. Koja zemlja je najvise puta ucestvovala u letnjim igrama
#
# # df1 = df1.groupby('Team')['Num of summer games'].sum().sort_values(ascending = False)
# # print(df1)
#
# # 2. Koja Africka zemlja je najvise puta ucestvovala u letnjim igrama
#
# # africa = df1[df1['Continent'] == 'Africa'].sort_values(by = 'Num of summer games',ascending = False).head(1)
# # print(africa)
#
# # 3. Koje zemlje su ucestvovale samo na letnjim igrama (a ni jednom na zimskim)
#
# # only_summer_games_countries = df1[df1['Num of winter games'] == 0]
# # print(only_summer_games_countries)
#
# # 4. Koliko ukupno puta su africke zemlje ucestvovale na svim igrama
#
# df1 = df1[df1['Continent'] == 'Africa']['Total num of all games'].sum()
# print('Africa: ',df1)
#
# # 5. Pronadji sve zemlje koje su ucestvovale ise puta na zimskim nego na letnjim igrama
#
# # df1 = df1[df1['Num of winter games'] > df1['Num of summer games']]
# # print('Countries which played more times on winter games than summer games:\n ',df1)
#
# # 6. Prosecan broj letnjih i zimskih igara po kontinentu
#
# avg_num_of_summer_and_winter = df1.groupby('Continent')[['Num of summer games','Num of winter games']].mean()
# print(avg_num_of_summer_and_winter)
#
# # 7. Broj drzava sa najmanjim brojem ukupnih ucesca
#
#
# # 8. Ukupan broj svih igara po kontinentu
#
total = df1.groupby('Continent')['Total num of all games'].sum()
print('Total num of all games per continent:\n',total)
# # print('')

# # 9. Koliko drzava ima po kontinentu
#
# num_of_contries_per_continent = df1['Continent'].value_counts()
# print('Number of countries per continent:\n',num_of_contries_per_continent)
# print('')
#
# # 10. drzave koje su ucestvovale vise od proseka svih igara
#
# average_total = df1['Total num of all games'].mean()
# print(average_total)
# print('')
# more_than_avg = df1[df1['Total num of all games'] > average_total]
# print('countries which participated more than avg:\n',more_than_avg[['Team','Total num of all games']])
# print('')
#
# # 11. Kontinent sa njvise ukupno odigranih igara
#
# total_per_cont = df1.groupby('Continent')['Total num of all games'].sum()
# print(total_per_cont.idxmax(), total_per_cont.max())
# print('')
#
# # 12. Zemlje sa nula ucestvovanja na letnjim i zimskim (posebno)
#
# countries_with_0_part_summer = df1[df1['Num of summer games'] == 0]
# print('Countries with zero participation in summer games:\n ', countries_with_0_part_summer)
# print('')
# countries_with_0_part_winter = df1[df1['Num of winter games'] == 0]
# print('Countries with zero participation in winter games:\n ', countries_with_0_part_winter['Team'])
# print('')


df1.to_csv('bez_medalja_olimpijske.csv', index= False)