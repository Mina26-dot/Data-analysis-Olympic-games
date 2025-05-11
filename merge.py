import pandas as pd
from Olympic_Games import olympics_years
from Olympic_Games import medalje_tabela_olimpijske

df1 = pd.read_csv('medalje_tabela_olimpijske.csv')
df2 = pd.read_csv('olympics_years.csv')
df3 = pd.read_csv('spec_delegacije_nije_stvarna_drzava.csv')
df4 = pd.read_csv('neaktivne(ugasene)zemlje.csv')

merge = pd.merge(df1,df2,left_on='CleanCountry',right_on='NOC',how='outer')
print(merge.columns)

merge['CleanCountry'] = merge['CleanCountry'].where(~merge['CleanCountry'].duplicated(),'')
print(merge[['CleanCountry','Gold years','Year']])

merge['NOC'] = merge['NOC'].where(~merge['NOC'].duplicated(),'')
print(merge[['NOC','Gold years','Year']])

gold = merge.groupby('CleanCountry')['Total gold medals'].first().sum()
print('GOLD: \n',gold)

silver = merge.groupby('CleanCountry')['Total silver medals'].first().sum()
print('Silver: ',silver)

# print(merge['Silver'].sum())
# print(merge['Total'].sum())

# merge['Year'] = pd.to_datetime(merge['Year'], format='%Y-%m-%d')
# merge['Year'] = merge['Year'].dt.year
merge['Year'] = pd.to_numeric(merge['Year'], errors='coerce').astype('Int64')

# print(merge['Year'].unique())

print('Year:\n',merge['Year'])


merge[merge.select_dtypes(include=['number']).columns] = merge.select_dtypes(include=['number']).fillna(0)
merge[merge.select_dtypes(include=['object']).columns] = merge.select_dtypes(include=['object']).fillna('UNKNOWN')

print(merge.isna().sum())

# print(merge[['CleanCountry','Gold','Year']].head(50))


# print(merge[merge.duplicated()])
# # merge.drop_duplicates()
#
# dupl = merge[merge.duplicated(keep=False)]
# print(dupl.iloc[0] == dupl.iloc[1])

num_of_columns = len(merge.columns)
print(num_of_columns)
print(merge.columns)


#+++++++++++++++++++++ SPECIAL DELEGATIONS AND DEFUNCT COUNTRIES (STATUS) ++++++++++++++++++++++++++++


special_delegations = set(df3['Team'])
defunct_countries = set(df4['Team'])

def get_status(team):
    if team in special_delegations:
        return 'special_delegation'
    elif team in defunct_countries:
        return 'defunct'
    else:
        return 'active'

merge['Status'] = merge['Team'].apply(get_status)

merge['Team'] = merge['Team'].where(~merge['Team'].duplicated(),'')
print(merge[['Team','Status']].value_counts().head(50))


merge.to_csv('merge.csv', index=False)
