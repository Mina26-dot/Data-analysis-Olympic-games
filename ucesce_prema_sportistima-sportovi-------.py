import pandas as pd
import matplotlib.pyplot as plt

url = 'https://www.olympedia.org/statistics/participation'
tables = pd.read_html(url)

print(f'Broj ucitanih tabela: {len(tables)}')

df = tables[0]

print(df['Sport(s)'])

df['Sport(s)'] = df['Sport(s)'].str.split('/')
df = df.explode('Sport(s)')

# era
df['Era'] = df['Era'].str.replace('â', '-', regex=False)

def parse_year_range(era):
    try:
        start, end = era.split('-')
        return int(start), int(end)
    except ValueError:
        return None

df['Era'] = df['Era'].apply(parse_year_range)
df = df[df['Era'].notnull()]
df[['Start Year', 'End Year']] = pd.DataFrame(df['Era'].to_list(), index=df.index)

print(df.columns)

column_rename = {
    'Nation(s)': 'Nation',
    'Sport(s)': 'Sport',
    'Role(s)': 'Role'
}
df = df.rename(columns=column_rename)


# - Analiza: Koji sportovi su vremenom postajali popularniji (po broju ucesnika)



df['Years'] = df.apply(lambda row: list(range(row['Start Year'], row['End Year'] +1)) if pd.notnull(row['Start Year']) and pd.notnull(row['End Year']) else [], axis=1)
df = df.explode('Years')

print(df['Sport'].unique())

sport_map = {
    "EJP": "Judo",
    "SHO": "Shooting",
    "SAL": "Sailing",
    "GAR": "Artistic Gymnastics",
    "EVE": "Equestrian Eventing",
    "ATH": "Athletics",
    "CSP": "Canoe Sprint",
    "SJP": "Ski Jumping",
    "BTH": "Biathlon",
    "CCS": "Cross-Country Skiing",
    "MTB": "Mountain Bike",
    "SSK": "Speed Skating",
    "ROW": "Rowing",
    "LUG": "Luge",
    "FBL": "Football",
    "EDR": "Equestrian Dressage",
    "CTR": "Canoe Slalom",
    "CRD": "Curling",
    "FEN": "Fencing",
    "TTE": "Table Tennis",
    "TEN": "Tennis"
}

df['Sport_full'] = df['Sport'].map(sport_map)
print(df['Sport_full'])

popularity_by_year = df.groupby(['Years', 'Sport_full'])['Athlete'].nunique().reset_index(name='Num_athletes')
pivot_df = popularity_by_year.pivot(index='Years', columns='Sport_full', values='Num_athletes')

# pivot_df.plot(kind='bar', stacked=True, figsize=(18, 8), cmap='tab20', width=0.8)
# plt.title('Popularity of Sports Over Time (by Number of Athletes)')
# plt.xlabel('Year')
# plt.ylabel('Number of Athletes')
# plt.legend(title='Sport', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.xticks(rotation=90, ha='right')
# plt.tight_layout()
# plt.show()

print(df.columns)



# Analiza zivotnog veka sportova:
# koji su stalno prisutni, a koji brzo nestaju?
#
# Vizualizacija prve i poslednje godine pojavljivanja po sportu.

olympic_years = [1896, 1900, 1904, 1908, 1912, 1920, 1924, 1928, 1932, 1936, 1948, 1952, 1956,
                 1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008,
                 2012, 2016, 2020]


sport_lifetime = df.groupby('Sport_full').agg(
    first_year=('Start Year', 'min'),
    last_year=('End Year', 'max')
).reset_index()

sport_lifetime = sport_lifetime[sport_lifetime['first_year'] <= 2020]

# plt.figure(figsize=(14, 7))
#
# plt.plot(sport_lifetime['Sport_full'], sport_lifetime['first_year'], label='Prva godina', color='green', marker='o', linestyle='-', markersize=5, linewidth=1)
#
# plt.plot(sport_lifetime['Sport_full'], sport_lifetime['last_year'], label='Poslednja godina', color='red', marker='x', linestyle='-', markersize=5, linewidth=1)
#
# plt.title('Zivotni vek sportova na Olimpijadi (Prva i Poslednja godina)', fontsize=16)
# plt.xlabel('Sport', fontsize=12)
# plt.ylabel('Godina', fontsize=12)
# plt.xticks(rotation=90)
# plt.legend(title='Godina', loc='upper left')
# plt.tight_layout()
#
# plt.show()


print(df['Sport'])




# 10. Koje zemlje vise igraju u timskim, a koje u individualnim disciplinama?

team_sports = ['Football', 'Equestrian Eventing', 'Curling', 'Basketball', 'Handball', 'Volleyball', 'Rugby', 'Baseball/Softball']

individual_sports = ['Judo', 'Shooting', 'Sailing', 'Artistic Gymnastics', 'Athletics',
                     'Canoe Sprint', 'Ski Jumping', 'Biathlon', 'Cross-Country Skiing',
                     'Mountain Bike', 'Speed Skating', 'Rowing', 'Luge', 'Equestrian Dressage',
                     'Canoe Slalom', 'Fencing', 'Table Tennis', 'Tennis', 'Cycling']

nation_map = {
    'CAN': 'Canada',
    'LAT': 'Latvia',
    'URS': 'Soviet Union',
    'GEO URS EUN': 'Georgia, Soviet Union, Unified Team',
    'PER': 'Peru',
    'GER EUN UZB': 'Germany, Unified Team, Uzbekistan',
    'ITA': 'Italy',
    'SLO YUG': 'Slovenia, Yugoslavia',
    'DEN': 'Denmark',
    'ESP': 'Spain',
    'AUS': 'Australia',
    'ITA FRG': 'Italy, West Germany',
    'JPN': 'Japan',
    'GBR BAH': 'Great Britain, Bahamas',
    'BRA': 'Brazil',
    'GER': 'Germany',
    'FIN': 'Finland',
    'SUI': 'Switzerland',
    'GER FRG': 'Germany, West Germany',
    'BLR': 'Belarus',
    'RUS EUN': 'Russia, Unified Team',
    'AUS USA': 'Australia, USA',
    'BUL': 'Bulgaria',
    'NED': 'Netherlands',
    'BLR EUN': 'Belarus, Unified Team',
    'BEL': 'Belgium',
    'ARG': 'Argentina',
    'BEL NED': 'Belgium, Netherlands',
    'FRA': 'France',
    'HUN': 'Hungary',
    'NGR': 'Nigeria',
    'MGL': 'Mongolia',
    'JAM SLO': 'Jamaica, Slovenia',
    'IND': 'India',
    'SWE': 'Sweden',
    'USA': 'United States of America',
    'CRO YUG': 'Croatia, Yugoslavia',
    'IOA KUW': 'India Olympic Association, Kuwait',
    'POR': 'Portugal'
}

df['Nation'] = df['Nation'].replace(nation_map)

def classify_sport(sport):
    if sport in team_sports:
        return 'Team'
    elif sport in individual_sports:
        return 'Individual'
    else:
        return 'Other'

df['Sport_Type'] = df['Sport_full'].apply(classify_sport)

sport_classification = df[['Sport_full', 'Sport_Type']].drop_duplicates().sort_values(by='Sport_Type')

print("Sportovi i njihova klasifikacija (Timski vs Individualni):")
print(sport_classification)

participations_by_type = df.groupby(['Nation', 'Sport_Type']).size().unstack(fill_value=0)

print("\nBroj ucesca po zemljama i sportovima:")
print(participations_by_type)

participations_by_type.plot(kind='bar', stacked=True, figsize=(14, 8))
plt.title('Ucesce zemalja u timskim i individualnim sportovima')
plt.xlabel('Zemlja')
plt.ylabel('Broj ucesca')

plt.xticks(rotation=90, ha='center')
plt.tight_layout()
# plt.show()
#
# unique_nations = df['Nation'].unique()
#
# print(unique_nations)

print(df)
# df.to_csv('ucesce_prema_sportistima-sportovi.csv')