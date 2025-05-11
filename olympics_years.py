import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('olympics_years.csv')
df = pd.DataFrame(data)

print(df.columns)

df.columns.values[3] = 'Gold years'
df.columns.values[4] = 'Silver years'
df.columns.values[5] = 'Bronze years'
df.columns.values[6] = 'Total years'





df['Year'] = df['Year'].astype(int)


# SAD je bojkotovao Rusiju 1980
# Rusija je bojkotovala 1984

boycott_years = df[df['Year'].isin([1984])]
boycott_performance = boycott_years.groupby('Year')['Total years'].sum()
print('Boycott by Russia:\n',boycott_performance)

sssr_countries = ['USSR','Russia','Ukraine','Kazakhstan','Armenia','Belarus','Georgia','Uzbekistan','Azerbaijan','Moldova']
sssr_data = df[df['NOC'].isin(sssr_countries)]
sssr_performance = sssr_data.groupby(['Year','NOC'])['Total years'].sum().reset_index()

before_ussr = df[(df['NOC'] =='Soviet Union') & (df['Year'] < 1991)]
after_ussr = sssr_performance[sssr_performance['Year'] >= 1991]

print('BEFORE: \n',before_ussr.groupby(['NOC','Gold years','Silver years','Bronze years'])['Total years'].sum())
print('')
print('AFTER: \n',after_ussr.groupby('NOC')['Total years'].sum())

plt.figure(figsize=(10,6))
df.groupby('Year').agg({'Total years':'sum'}).plot(kind='line')
plt.title('Total medals trend over the years')
plt.xlabel('Year')
plt.ylabel('Total medals')
plt.grid(True)
# plt.show()


#+++++++++++++++++++++++++++++++ pre i posle raspada USSR-a++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


before_ussr_total = before_ussr.groupby('NOC')['Total years'].sum()
after_ussr_total = after_ussr.groupby('NOC')['Total years'].sum()

comparison_df = pd.DataFrame({
    'Before 1991' : before_ussr_total,
    'After 1991' : after_ussr_total
}).fillna(0)

plt.figure(figsize=(10,6))
comparison_df.plot(kind='bar',figsize=(12,6))
plt.title('Comparison of Total Medals: USSR Successor states before and after 1991')
plt.xlabel('Country (NOC)')
plt.ylabel('Total medals')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
# plt.show()

successors = ['Russia','Ukraine','Belarus','Kazakhstan','Uzbekistan','Georgia','Azerbaijan','Armenia','Moldova']
successors_data = df[(df['NOC'].isin(successors)) & (df['Year'] >=1992)]
total_successors_medals = successors_data.groupby('Year')['Total years'].sum().reset_index()

ussr_data = df[(df['NOC'] == 'USSR') & (df['Year'] < 1992)]
ussr_total = ussr_data[['Year','Total years']]

combined = pd.concat([ussr_total,total_successors_medals])

plt.figure(figsize=(12,6))
plt.bar(combined['Year'],combined['Total years'], color='blue')
plt.title('USSR vs Successor states (total medals per year)')
plt.xlabel('Year')
plt.ylabel('Total medals')
plt.xticks(rotation=45)
plt.grid(axis = 'y')
# plt.show()

# koje zemlje su posle rapsada napredovale itd...

grouped = successors_data.groupby(['Year','NOC'])['Total years'].sum().reset_index()

pivot_df = grouped.pivot(index = 'Year', columns='NOC', values='Total years').fillna(0)

plt.figure(figsize=(14,7))
for country in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[country], marker='o', label=country)

plt.title('Olympic medal trend for USSR successor states (1992-2024)')
plt.xlabel('Year')
plt.ylabel('Total medals')
plt.legend(title='Country')
plt.grid(True)
plt.tight_layout()
# plt.show()

#+++++++++++++++++++++++++++++++++++++++++ JUGOSLAVIJA +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def yug_successors(row):
    if row['NOC'] == 'YUG' and row['Year'] < 1991:
        return 'Yugoslavia (before 1992)'
    elif row['NOC'] in ['YUG','SCG'] and row['Year'] >= 1992 and row['Year'] <= 2004:
        return 'Serbia and Montenegro (1996-2004)'
    elif row['NOC'] in ['Serbia', 'Montenegro', 'Croatia', 'Slovenia', 'Bosnia ans Herzegovina','North Macedonia','Kosovo']:
        return row['NOC']
    else:
        return None

df['Yug_group'] = df.apply(yug_successors, axis = 1)
df_yugo = df[df['Yug_group'].notna()]

grouped = df_yugo.groupby(['Year','Yug_group'])['Total years'].sum().reset_index()

pivot = grouped.pivot(index='Year',columns='Yug_group', values='Total years').fillna(0)

plt.figure(figsize=(12,6))
pivot.plot(marker='o')
plt.title('Medal counts of Yugoslavia and successor states over time')
plt.xlabel('Year')
plt.ylabel('Total medals')
plt.grid(True)
plt.legend(title = 'Country-group')
plt.tight_layout()
# plt.show()

# UKRAJINA :   ++++++++++++++++++++Ukrajina na olimpijskim pre i u toku rata +++++++++++++++++++++++++++++++++++++++++

ukraine_before_war = df[(df['NOC'] == 'Ukraine') & (df['Year'] < 2024)]
print('Ukraine before war:\n',ukraine_before_war)
print('')
ukraine_during_the_war = df[(df['NOC'] == 'Ukraine') & (df['Year'] >= 2022)]
print('Ukraine during war:\n',ukraine_during_the_war)
print('')
ukraine_all = df[df['NOC'] == 'Ukraine'].copy()
ukraine_all['Year'] = ukraine_all['Year']

plt.figure(figsize=(12, 6))

# Zlatne medalje
plt.plot(ukraine_all['Year'], ukraine_all['Gold years'], marker='o', label='Zlatne', color='gold')

# Srebrne medalje
plt.plot(ukraine_all['Year'], ukraine_all['Silver years'], marker='o', label='Srebrne', color='silver')

# Bronzane medalje
plt.plot(ukraine_all['Year'], ukraine_all['Bronze years'], marker='o', label='Bronzane', color='#cd7f32')

plt.axvline(x=2022, color='red', linestyle='--', linewidth=1.5, label='Pocetak rata (2022)')
plt.title('Ukrajina: Broj osvojenih medalja na OI (po vrstama, pre i tokom rata)', fontsize=14)
plt.xlabel('Godina', fontsize=12)
plt.ylabel('Broj medalja', fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()
# plt.show()

#+++++++++++++++++++++++++++++++++++ Afrticke zemlje pre, u toku i nakon ratova +++++++++++++++++++++++++++++++++++++

# Alzir je bio u ratu za nezavisnost protiv Francuske od 1954. do 1962. godine.
# U vreme kada su Olimpijske igre 1964. godine odrzane u Tokiju, Alzir je postao nezavisna drzava (1962).
# Olimpijske igre 1964: Alzir je ucestvovao kao samostalna zemlja na Olimpijadi

algeria_before_war = df[(df['NOC'] == 'Algeria') & (df['Year'] < 1962)]
print('Algeria before war:\n',algeria_before_war)
print('')

algeria_after_war = df[(df['NOC'] == 'Algeria') & (df['Year'] >= 1962)]
print('Algeria after war: \n',algeria_after_war)
print('')
algeria_df = df[df['NOC'] == 'Algeria'].copy()
algeria_df['Year'] = algeria_df['Year']
algeria_df['Total years'] = algeria_df['Gold years'] + algeria_df['Silver years'] + algeria_df['Bronze years']

# rat za nezavisnost 1954–1962

def war_period(year):
    if year < 1954:
        return 'Pre rata'
    elif 1954 <= year < 1962:
        return 'Tokom rata'
    else:
        return 'Posle rata'

algeria_df['Period'] = algeria_df['Year'].apply(war_period)

grouped = algeria_df.groupby(['Year', 'Period'])['Total years'].sum().reset_index()
plt.figure(figsize=(10, 6))

for period in grouped['Period'].unique():
    data = grouped[grouped['Period'] == period]
    plt.plot(data['Year'], data['Total years'], marker='o', label=period)

plt.title('Alzir – Medalje pre, tokom i posle rata za nezavisnost')
plt.xlabel('Godina')
plt.ylabel('Ukupno medalja')
plt.legend()
plt.grid(True)
plt.tight_layout()
# plt.show()



# Olimpijske igre 1980:
# Iako je zemlja bila u politickom i ratnom haosu,
# Etiopija je ucestvovala na Olimpijadi u Moskvi 1980. godine.


ethiopia_before_war = df[(df['NOC'] == 'Ethiopia') & (df['Year'] < 1974)]
print('Ethiopia before war:\n',ethiopia_before_war)
print('')

ethiopia_during_war = df[(df['NOC'] == 'Ethiopia') & (df['Year'] >= 1974) & (df['Year'] < 1991)]
print('Ethiopia during war:\n',ethiopia_during_war)
print('')


ethiopia_after_war = df[(df['NOC'] == 'Ethiopia') & (df['Year'] >= 1991)]
print('Ethiopia after war:\n',ethiopia_after_war)
print('')


ethiopia_before_war_sum = ethiopia_before_war.groupby('Year').sum()
ethiopia_during_war_sum = ethiopia_during_war.groupby('Year').sum()
ethiopia_after_war_sum = ethiopia_after_war.groupby('Year').sum()

def ethiopia_participation_status(row):
    year = row['Year'].year if isinstance(row['Year'], pd.Timestamp) else row['Year']
    noc = row['NOC']

    if noc != 'Ethiopia':
        return 'N/A'

    if year in [1976, 1984, 1988]:
        return 'Bojkot'
    elif year < 1974:
        return 'Pre rata'
    elif 1974 <= year < 1991:
        return 'Ucesce tokom rata'
    elif year >= 1991:
        return 'Posle rata'
    else:
        return 'Nepoznato'


df['Participation_Status'] = df.apply(ethiopia_participation_status, axis=1)
ethiopia_df = df[df['NOC'] == 'Ethiopia']
medals_by_status = ethiopia_df.groupby('Participation_Status')[['Gold years', 'Silver years', 'Bronze years']].sum()
print(medals_by_status)

medals_by_status.plot(kind='bar', figsize=(10, 6), colormap='viridis')
plt.title('Etiopija – Medalje po politicko-ratnim periodima')
plt.ylabel('Broj medalja')
plt.xlabel('Status')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
# plt.show()

#++++++++++++ zemlje koje su bile zvanicno iskljucene od strane MOK-a ili onemogucene zbog ratnih okolnosti+++++++++++++

# NISU SMELE (zvanicna zabrana ili posledica rata):

# 1920	Nemacka, Austrougarska (Austrija, Madjarska), Bugarska, Turska:	iskljucene zbog uloge u Prvom svetskom ratu
# 1948	Nemacka, Japan:	iskljucene nakon Drugog svetskog rata
# 1992	Savezna Republika Jugoslavija (Srbija i Crna Gora):	Zabrana zbog sankcija UN tokom rata u Jugoslaviji
# 2000	Avganistan	Iskljucen zbog talibanskog rezima (zenska prava, UN sankcije)

missing_data = [
    {'Year': 1920, 'NOC': 'Germany', 'Participation_Status': 'Excluded due to World War I (1920)'},
    {'Year': 1920, 'NOC': 'Austria', 'Participation_Status': 'Excluded due to World War I (1920)'},
    {'Year': 1920, 'NOC': 'Hungary', 'Participation_Status': 'Excluded due to World War I (1920)'},
    {'Year': 1920, 'NOC': 'Bulgaria', 'Participation_Status': 'Excluded due to World War I (1920)'},
    {'Year': 1920, 'NOC': 'Turkey', 'Participation_Status': 'Excluded due to World War I (1920)'},
    {'Year': 1948, 'NOC': 'Germany', 'Participation_Status': 'Excluded after World War II (1948)'},
    {'Year': 1948, 'NOC': 'Japan', 'Participation_Status': 'Excluded after World War II (1948)'},
    {'Year': 1992, 'NOC': 'Yugoslavia', 'Participation_Status': 'Excluded due to UN sanctions during the Yugoslav War (1992)'},
    {'Year': 2000, 'NOC': 'Afghanistan', 'Participation_Status': 'Excluded due to the Taliban regime (2000)'}
]

missing_df = pd.DataFrame(missing_data)
df = pd.concat([df, missing_df], ignore_index=True)

def participation_status(row):
    if row['Year'] == 1920 and row['NOC'] in ['Germany', 'Austria', 'Hungary', 'Bulgaria', 'Turkey']:
        return 'Excluded due to World War I (1920)'
    elif row['Year'] == 1948 and row['NOC'] in ['Germany', 'Japan']:
        return 'Excluded after World War II (1948)'
    elif row['Year'] == 1992 and row['NOC'] == 'Yugoslavia':
        return 'Excluded due to UN sanctions during the Yugoslav War (1992)'
    elif row['Year'] == 2000 and row['NOC'] == 'Afghanistan':
        return 'Excluded due to the Taliban regime (2000)'
    else:
        return 'Participated'

df['Participation_Status'] = df.apply(participation_status, axis=1)

germany = df[df['NOC'] == 'Germany']
print(germany)

print(df[['NOC','Participation_Status']])

#++++++++++++++++++++++++++++ IRSKA polse otcepljenja i VELIKA BRITANIJA sa i bez IRSKE ++++++++++++++++++++++++

# Do 1922. godine – Irska kao deo Britanske imperije
# Britaanija pre otcepljenja Irske/ pre 1922.
#
britain_before_1922 = df[(df['NOC'] == 'Great Britain') & (df['Year'] < 1922)]
print('Britain before the separation of Ireland:\n',britain_before_1922)
print('')

# Posle otcepljenja Irske 1922. Britanija

britain_after_1922 = df[(df['NOC'] == 'Great Britain') & (df['Year'] >= 1922)]
print('Britain after the separation of Ireland:\n', britain_after_1922)
print('')

# Irska nakon otcepljenja nakon 1922.

ireland_after_separation = df[(df['NOC'] == 'Ireland') & (df['Year'] > 1922)]
print(ireland_after_separation)
print('')

britain_before_1922_medals = britain_before_1922[['Gold years', 'Silver years','Bronze years']].sum()
britain_after_1922_medals = britain_after_1922[['Gold years', 'Silver years','Bronze years']].sum()

ireland_after_1922_medals = ireland_after_separation[['Gold years', 'Silver years','Bronze years']].sum()

print(f"Britain before 1922. year:\n{britain_before_1922_medals} medals")
print('')
print(f"Britain after 1922. year:\n{britain_after_1922_medals} medals")
print('')
print(f"Ireland after 1922. year:\n{ireland_after_1922_medals} medals")
print('')


britain_before_1922_medals = britain_before_1922[['Gold years', 'Silver years', 'Bronze years']].sum()
britain_after_1922_medals = britain_after_1922[['Gold years', 'Silver years', 'Bronze years']].sum()
ireland_after_1922_medals = ireland_after_separation[['Gold years', 'Silver years', 'Bronze years']].sum()

print(f"Britain before 1922:\n{britain_before_1922_medals} medals")
print('')
print(f"Britain after 1922:\n{britain_after_1922_medals} medals")
print('')
print(f"Ireland after 1922:\n{ireland_after_1922_medals} medals")
print('')

britain_before_1922_medals = britain_before_1922.groupby('Year')[['Gold years', 'Silver years', 'Bronze years']].sum()
britain_after_1922_medals = britain_after_1922.groupby('Year')[['Gold years', 'Silver years', 'Bronze years']].sum()
ireland_after_separation_medals = ireland_after_separation.groupby('Year')[['Gold years', 'Silver years', 'Bronze years']].sum()

britain_before_1922_medals['Total years'] = britain_before_1922_medals.sum(axis=1)
britain_after_1922_medals['Total years'] = britain_after_1922_medals.sum(axis=1)
ireland_after_separation_medals['Total years'] = ireland_after_separation_medals.sum(axis=1)


plt.figure(figsize=(10, 6))
plt.plot(britain_before_1922_medals.index, britain_before_1922_medals['Total years'], label='Britain before 1922', color='blue', linestyle='-', marker='o')
plt.plot(britain_after_1922_medals.index, britain_after_1922_medals['Total years'], label='Britain after 1922', color='green', linestyle='--', marker='x')
plt.plot(ireland_after_separation_medals.index, ireland_after_separation_medals['Total years'], label='Ireland after 1922', color='red', linestyle='-.', marker='s')
plt.xlabel('Year')
plt.ylabel('Total Medals')
plt.title('Total Medals Over Time: Britain and Ireland (Before and After 1922)')
plt.legend()
plt.tight_layout()
# plt.show()

#+++++++++++++++++++++++++++++++++ Cehoslovacka (Ceska i Slovacka) pre i posle raspada +++++++++++++++++++++++++++++++++

chez_before_sep_before_1993 = df[(df['NOC'] == 'Czechoslovakia') & (df['Year'] < 1993)]
chez_before_separation = chez_before_sep_before_1993.groupby('Year')[['NOC','Gold years','Silver years','Bronze years','Total years']].sum().reset_index()

print('Czechoslovakia before separation (before 1993): \n',chez_before_separation)
print('')

slovakia_after_1993 = df[(df['NOC'] == 'Slovakia') & (df['Year'] > 1993)]
slovakia_after_separation = slovakia_after_1993.groupby('Year')[['NOC','Gold years','Silver years','Bronze years','Total years']].sum().reset_index()
print('Slovakia after 1993.:\n',slovakia_after_separation)
print('')

chez_republic_after_1993 = df[(df['NOC'] == 'Czech Republic') & (df['Year'] > 1993)]
chez_republic_after_separation = chez_republic_after_1993.groupby('Year')[['NOC','Gold years','Silver years','Bronze years','Total years']].sum().reset_index()
print('Czech Republic after 1993.:\n', chez_republic_after_separation)
print('')

plt.figure(figsize=(14, 8))

plt.plot(chez_before_separation['Year'], chez_before_separation['Gold years'], label='Czechoslovakia - Gold', color='gold', linestyle='-')
plt.plot(chez_before_separation['Year'], chez_before_separation['Silver years'], label='Czechoslovakia - Silver', color='silver', linestyle='--')
plt.plot(chez_before_separation['Year'], chez_before_separation['Bronze years'], label='Czechoslovakia - Bronze', color='#cd7f32', linestyle=':')

plt.plot(slovakia_after_separation['Year'], slovakia_after_separation['Gold years'], label='Slovakia - Gold', color='darkgoldenrod', linestyle='-')
plt.plot(slovakia_after_separation['Year'], slovakia_after_separation['Silver years'], label='Slovakia - Silver', color='gray', linestyle='--')
plt.plot(slovakia_after_separation['Year'], slovakia_after_separation['Bronze years'], label='Slovakia - Bronze', color='saddlebrown', linestyle=':')

plt.plot(chez_republic_after_separation['Year'], chez_republic_after_separation['Gold years'], label='Czech Republic - Gold', color='orange', linestyle='-')
plt.plot(chez_republic_after_separation['Year'], chez_republic_after_separation['Silver years'], label='Czech Republic - Silver', color='lightgray', linestyle='--')
plt.plot(chez_republic_after_separation['Year'], chez_republic_after_separation['Bronze years'], label='Czech Republic - Bronze', color='peru', linestyle=':')

plt.title('Olympic Medal Trends: Czechoslovakia, Czech Republic, and Slovakia')
plt.xlabel('Year')
plt.ylabel('Number of Medals')
plt.legend(loc='upper left')
plt.grid(True)
plt.tight_layout()
# plt.show()

#+++++++++++++++++++++++++++++++++++++ NEMACKA pre i posle ujedninjenja 1990. ++++++++++++++++++++++++++++++++++++++++++++++++

# pre ujedinjenja

germany = df[df['NOC'] == 'West Germany']
print(germany)

# zapadna nemacka pre 1990

west_germany_before_1990 = df[(df['NOC'] == 'West Germany') & (df['Year'] < 1990)]
west_germany_medals_before_1990 = west_germany_before_1990.groupby('Year')[['Gold years','Silver years','Bronze years','Total years']].sum().reset_index()
west_germany_medals_before_1990_total = west_germany_before_1990.groupby('NOC')[['Gold years','Silver years','Bronze years','Total years']].sum().reset_index()

print('West Germany before 1990.:\n', west_germany_medals_before_1990)
print('')
print('Total num of medal before 1990 for West Germany:\n', west_germany_medals_before_1990_total)
print('')

# istocna nemacka pre 1990

east_germany_before_1990 = df[(df['NOC'] == 'East Germany') & (df['Year'] < 1990)]
east_germany_medals_before_1990 = east_germany_before_1990.groupby('Year')[['Gold years','Silver years','Bronze years','Total years']].sum().reset_index()
east_germany_medals_before_1990_total = east_germany_before_1990.groupby('NOC')[['Gold years','Silver years','Bronze years','Total years']].sum().reset_index()

print('East Germany before 1990.:\n', east_germany_medals_before_1990)
print('')
print('Total num of medal before 1990 for East Germany:\n', east_germany_medals_before_1990_total)
print('')

sum_medals_east_and_west = east_germany_medals_before_1990_total +  west_germany_medals_before_1990_total
print(sum_medals_east_and_west)


germany_after_1990 = df[(df['NOC'] == 'Germany') & (df['Year'] > 1990)]
germany_medals_after_1990 = germany_after_1990.groupby('Year')[['Gold years','Silver years','Bronze years','Total years']].sum().reset_index()
germany_medals_after_1990_total = germany_after_1990.groupby('NOC')[['Gold years','Silver years','Bronze years','Total years']].sum().reset_index()

print('Germany medals after 1990.:\n', germany_medals_after_1990)
print('')
print('Total num of all medals for Germany after 1990.:\n',germany_medals_after_1990_total)

west_germany_before_total = [
    west_germany_medals_before_1990_total['Gold years'].values[0],
    west_germany_medals_before_1990_total['Silver years'].values[0],
    west_germany_medals_before_1990_total['Bronze years'].values[0]
]

east_germany_before_total = [
    east_germany_medals_before_1990_total['Gold years'].values[0],
    east_germany_medals_before_1990_total['Silver years'].values[0],
    east_germany_medals_before_1990_total['Bronze years'].values[0]
]

germany_after_total = [
    germany_medals_after_1990_total['Gold years'].values[0],
    germany_medals_after_1990_total['Silver years'].values[0],
    germany_medals_after_1990_total['Bronze years'].values[0]
]

labels = ['Gold years', 'Silver years', 'Bronze years']

x = np.arange(len(labels))

bar_width = 0.25

fig, ax = plt.subplots(figsize=(12, 6))

bar1 = ax.bar(x - bar_width, west_germany_before_total, bar_width, label='West Germany Before 1990', color='b')
bar2 = ax.bar(x, east_germany_before_total, bar_width, label='East Germany Before 1990', color='r')
bar3 = ax.bar(x + bar_width, germany_after_total, bar_width, label='Unified Germany After 1990', color='g')

ax.set_xlabel('Medal Types')
ax.set_ylabel('Total Medals')
ax.set_title('Total Olympic Medals for Different Germanys: Before and After 1990')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.tight_layout()
plt.show()

total_num_of_medals = df['Total years'].sum()
print(total_num_of_medals)
print('Silver',df['Silver years'].sum())

df.to_csv('olympics_years.csv', index = False)