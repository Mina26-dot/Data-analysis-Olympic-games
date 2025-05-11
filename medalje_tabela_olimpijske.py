import pandas as pd
import pycountry
import pycountry_convert as pc
import re
import numpy as np

def load_and_clean_data():
    url = 'https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table'
    tables = pd.read_html(url)
    df = tables[1]
    df.to_csv('olimpic.csv', index=False)
    df = df.reset_index()
    df.columns = df.columns.droplevel(1)
    df.columns.values[0] = 'Index'
    df.columns.values[1] = 'Team'
    df.columns.values[2] = 'Num of summer games'
    df.columns.values[3] = 'Summer gold medals'
    df.columns.values[4] = 'Summer silver medals'
    df.columns.values[5] = 'Summer bronze medals'
    df.columns.values[6] = 'Total summer medals'
    df.columns.values[7] = 'Num of winter games'
    df.columns.values[8] = 'Winter gold medals'
    df.columns.values[9] = 'Winter silver medals'
    df.columns.values[10] = 'Winter bronze medals'
    df.columns.values[11] = 'Total winter medals'
    df.columns.values[12] = 'Total number of Games'
    df.columns.values[13] = 'Total gold medals'
    df.columns.values[14] = 'Total silver medals'
    df.columns.values[15] = 'Total bronze medals'
    df.columns.values[16] = 'Total of all medals'
    df.loc[:, "Team"] = df["Team"].apply(lambda x: re.sub(r"\s*\(.*?\)|\s*\[.*?/]", "", x).strip())
    df3 = pd.read_csv('spec_delegacije_nije_stvarna_drzava.csv')
    df4 = pd.read_csv('neaktivne(ugasene)zemlje.csv')
    df['Team'] = df['Team'].apply(lambda x: re.sub(r"(\s*\[.*?\]|\s*\(.*?\))+", "", x).strip())
    df = df.drop(162)
    return df, df3, df4

def basic_stats(df):
    print(df['Team'])
    print('Total gold medals:', df['Total gold medals'].sum())
    print('Total silver medals:', df['Total silver medals'].sum())
    print('Total bronze medals:', df['Total bronze medals'].sum())
    print('Total number of medals:', df['Total of all medals'].sum())

def top_medal_winners(df):
    print('Top 10 countries with the most num of medals:\n', df.sort_values(by='Total of all medals', ascending=False).head(10))
    print(df[['Team','Total gold medals']])
    print(df[['Team','Total silver medals']])
    print(df[['Team','Total bronze medals']])

def advanced_metrics(df):
    df['Avg_num_of_medals_per_game'] = df['Total of all medals']/df['Total number of Games']
    print('Average num of medals per game:\n', df['Avg_num_of_medals_per_game'].round())
    df['Percent of gold medals'] = (df['Total gold medals'] / df['Total of all medals'])*100
    df['Percent of silver medals'] = (df['Total silver medals'] / df['Total of all medals'])*100
    df['Percent of bronze medals'] = (df['Total bronze medals'] / df['Total of all medals'])*100
    print(df['Percent of gold medals'])
    print(df['Percent of silver medals'])
    print(df['Percent of bronze medals'])

def add_continents(df):
    def continent_of_country(country):
        try:
            code = pycountry.countries.lookup(country).alpha_2
            continent_code = pc.country_alpha2_to_continent_code(code)
            return pc.convert_continent_code_to_continent_name(continent_code)
        except:
            return 'Unknown'

    df['Continent'] = df['Team'].apply(continent_of_country)
    print('Continent', df['Continent'].head(50))
    print(df[['Team','Continent']].head(50))
    return df

def continent_analysis(df):
    print(df[df['Continent'] == 'Africa'])
    print('Only bronze medals:\n', df[(df['Continent'] == 'Africa') & (df['Total bronze medals'] > 0) &
                                     (df['Total gold medals'] ==0) & (df['Total silver medals'] ==0)])
    print('Total number of all medals per continent\n', df.groupby('Continent')['Total of all medals'].sum())
    print('Total number of gold medals per continent\n', df.groupby('Continent')['Total gold medals'].sum())
    print('Total number of bronze medals per continent\n', df.groupby('Continent')['Total bronze medals'].sum())
    print('Total number of silver medals per continent\n', df.groupby('Continent')['Total silver medals'].sum())
    print(df.groupby('Continent')['Total bronze medals'].mean())
    print(df['Total gold medals'].sort_values(ascending=False).head())
    print(df['Total bronze medals'].sort_values(ascending=False).head())
    print(df['Total silver medals'].sort_values(ascending=False).head())

def country_filtering(df):
    print(df[df['Total of all medals'] == 0])
    print(df[df['Total bronze medals'] > df['Total silver medals']])
    print('Aevarge of medals per country\n', df.groupby('Team')['Total of all medals'].mean())
    print('Countries with minimum one gold medal\n', df[df['Total gold medals'] > 0])
    print(df[df['Total bronze medals'] > (df['Total gold medals'] + df['Total silver medals'])])
    print('Countries with no gold medals but with bronze and silver\n', df[(df['Total gold medals'] == 0) &
          (df['Total silver medals'] > 0) & (df['Total bronze medals'] > 0)])

def assign_categories(df, df3, df4):
    special_delegations = set(df3['Team'])
    defunct_countries = set(df4['Team'])

    def get_status(team):
        if team in special_delegations:
            return 'special delegation'
        elif team in defunct_countries:
            return 'defunct'
        else:
            return 'active'

    df['Category'] = df['Team'].apply(get_status)
    df['Team'] = df['Team'].where(~df['Team'].duplicated(),'')
    print(df[['Team','Category']].head(7))

    rucno_kontinenti = {
        'Australasia': 'Oceania',
        'Bohemia': 'Europe',
        'British West Indies': 'North America',
        'Czechoslovakia': 'Europe',
        'United Team of Germany': 'Europe',
        'East Germany': 'Europe',
        'West Germany': 'Europe',
        'Kosovo': 'Europe',
        'Netherlands Antilles': 'North America',
        'Russian Empire': 'Europe',
        'Soviet Union': 'Europe',
        'Serbia and Montenegro': 'Europe',
        'Chinese Taipei': 'Asia',
        'Virgin Islands': 'North America',
        'Yugoslavia': 'Europe'
    }

    df.loc[df['Continent'] == 'Unknown', 'Continent'] = df['Team'].map(rucno_kontinenti)
    df.loc[df['Continent'].isna(), 'Continent'] = 'Multiple Continents'
    return df


def medal_scores(df):
    df['Winter medal score'] = (
            df['Winter gold medals'] * 3 + df['Winter silver medals'] * 2 + df['Winter bronze medals']
    )
    df['Summer medal score'] = (
            df['Summer gold medals'] * 3 + df['Summer silver medals'] * 2 + df['Summer bronze medals']
    )
    df['Combined medal score'] = (
            df['Total gold medals'] * 3 + df['Total silver medals'] * 2 + df['Total bronze medals']
    )

    print(df[df['Num of winter games'] != 0][['Team', 'Continent', 'Winter medal score']])
    print(df[df['Num of summer games'] != 0][['Team', 'Continent', 'Summer medal score']])
    print(df[df['Num of summer games'] != 0][['Team', 'Continent', 'Combined medal score']])

    return df

def final_processing(df):
    df.loc[df["Team"] == "Turkey", "Continent"] = "Europe"
    df["Winter medals per Game"] = df["Total winter medals"] / df["Num of winter games"]
    df["Winter score per Game"] = df["Winter medal score"] / df["Num of winter games"]
    df["Winter gold Share"] = np.where(df["Total winter medals"] != 0,
                                       df["Winter gold medals"] / df["Total winter medals"], np.nan)
    df["Summer medals per Game"] = df["Total summer medals"] / df["Num of summer games"]
    df["Summer score per Game"] = df["Summer medal score"] / df["Num of summer games"]
    df["Summer gold Share"] = np.where(df["Total summer medals"] != 0,
                                       df["Summer gold medals"] / df["Total summer medals"], np.nan)
    print(df.isnull().sum())
    df = df.fillna(0)
    print(df.isnull().sum())

    nordic_teams = ["Norway", "Sweden", "Finland", "Denmark", "Iceland"]
    df["Group"] = "Other"
    df.loc[df["Team"].isin(nordic_teams), "Group"] = "Nordic"
    df.loc[(df["Continent"] == "Europe") & (~df["Team"].isin(nordic_teams)), "Group"] = "Rest of Europe"
    df.to_csv('medalje_tabela_olimpijske.csv', index=False)

def main():
    df, df3, df4 = load_and_clean_data()
    basic_stats(df)
    top_medal_winners(df)
    advanced_metrics(df)
    df = add_continents(df)
    continent_analysis(df)
    country_filtering(df)
    df = assign_categories(df, df3, df4)
    df = medal_scores(df)
    final_processing(df)

if __name__ == '__main__':
    main()




