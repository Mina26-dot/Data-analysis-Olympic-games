import pandas as pd

url = 'https://en.wikipedia.org/wiki/Lists_of_Olympic_medalists#Summer_Olympic_sports'
tables = pd.read_html(url)
df = tables[1]
df = df.reset_index(drop = True)
df.columns = df.columns.droplevel(1)

df.columns.values[0] = 'Discipline'
df.columns.values[1] = 'Contested'
df.columns.values[2] = 'Num of olympics up to 2024'
df.columns.values[3] = 'Medal events in 2024'
df.columns.values[4] = 'Gold medals awarded'
df.columns.values[5] = 'Silver medals awarded'
df.columns.values[6] = 'Bronze medals awarded'
df.columns.values[7] = 'Total medals awarded'
df.columns.values[8] = 'Athlete(s) with the most medals\n(gold–silver–bronze)'
df.columns.values[9] = 'Athlete(s) with the most gold medals'

print(df.columns)
print(df.isnull().sum())
df = df.fillna('Unknown')
print(df.isnull().sum())
print('')

# 1. Koliko ukupno disciplina postoji

total_num_of_disciplines = df['Discipline'].count()
print('Total number of disciplines:\n',total_num_of_disciplines)
print('')

# 2. Kolika je prosecna vrednost dodeljenih zlatnih medalja po disciplini

# avg_num_of_gold_per_disc = df.groupby('Discipline')['Gold medals awarded'].mean()
# print('Average num of gold medals awarded per discipline:\n',avg_num_of_gold_per_disc.sort_values(ascending = False))
# print('')

# 3. Koje tri discipline imaju najvise ukupno dodeljenih medalja?

# three_disc_with_most_awarded_medals = df.groupby('Discipline')['Total medals awarded'].sum().sort_values(ascending = False).head(3)
# print('Three disciplines with the most awarded medals:\n',three_disc_with_most_awarded_medals)
# print('')

# 4. Koje discipline su imale najmanje zlatnih medalja

# disc_with_smallest_num_of_medals = df.groupby('Discipline')['Gold medals awarded'].sum().sort_values(ascending = True)
# print('Disciplines with the smallest num of gold medals:\n',disc_with_smallest_num_of_medals)
# print('')

# 5. Pronadji discipline koje imaju vise od 10 medalja u svakoj kategoriji (gold, silver, bronze).

gold_more_than_10 = df[df['Gold medals awarded'] > 10]
silver_more_than_10 = df[df['Silver medals awarded'] > 10]
bronze_more_than_10 = df[df['Bronze medals awarded'] > 10]

print('gold_more_than_10: ', gold_more_than_10[['Discipline','Gold medals awarded']])
print('silver_more_than_10: ', silver_more_than_10[['Discipline','Silver medals awarded']])
print('bronze_more_than_10: ', bronze_more_than_10[['Discipline','Bronze medals awarded']])
print('')

# 6. Izdvoj discipline gde je broj medalja u 2024. jednak ukupnom broju dodeljenih medalja.

this = df[df['Medal events in 2024'] == df['Total medals awarded']]
print(this['Discipline'])


# 7. Grupisi discipline po broju olimpijskih ciklusa i izračunaj prosecan broj medalja po grupi.

group = df.groupby('Num of olympics up to 2024')['Total medals awarded'].mean()
print(group)
print('')


# 8. Koliko ukupno medalja su osvojili svi najuspesniji sportisti zajedno (saberi njihove medalje)?

total = df.groupby('Athlete(s) with the most gold medals')['Total medals awarded'].sum()
print('Best athletes with total num of all medals ',total)
print('')

# 9. Pronadji da li postoji disciplina u kojoj je broj dodeljenih medalja manji od broja medal događaja u 2024.

disc = df[df['Total medals awarded'] < df['Medal events in 2024']]
print('DISC:',disc['Discipline'])
print('')

# 10. Proveri da li je zbir svih dodeljenih zlatnih, srebrnih i
# bronzanih medalja jednak ukupnom broju medalja u tabeli.

total_sum = df['Total medals awarded'].sum()
print(total_sum)
medal_sum = (df['Gold medals awarded'] + df['Silver medals awarded'] + df['Bronze medals awarded']).sum()
print(medal_sum)
if total_sum == medal_sum:
    print('Total is correct.')
else:
    print('Total does not match.')
print('')

# 11. Pronadji ukupan broj razlicitih disciplina u tabeli.

unique = df['Discipline'].unique()
print(len(unique))


# 12. Izdvoj discipline koje su bile deo vise od 10 Olimpijskih igara

more_than_10 = df[df['Num of olympics up to 2024'] > 10]
print(more_than_10)

# 13. Prikazi 5 disciplina sa najvise osvojenih ukupnih medalja u 2024

five_disc = df.groupby('Discipline')['Total medals awarded'].sum().sort_values(ascending=False).head(5)
print(five_disc)
print('')

# 14. Pronadji disciplinu sa najvise dodeljenih zlatnih medalja

disc_most_gold = df.groupby('Discipline')['Gold medals awarded'].sum().sort_values(ascending=False).head(1)
print(disc_most_gold)
print('')

# 15. Izracunaj koliko odsto ukupnih medalja cine zlatne medalje

gold_total = df['Gold medals awarded'].sum()
total_medals = df['Total medals awarded'].sum()

perc = round((gold_total / total_medals) * 100, 2)
print(f"Procenat zlatnih medalja: {perc}%")
print('')


# 16. Prikazi sve discipline koje su bile deo više od 20 Olimpijada

disc_on_more_than_20_og = df[df['Num of olympics up to 2024'] > 20]
print(disc_on_more_than_20_og)



# 17. Prikazi sve discipline gde ime sportiste sa najvise medalja sadrzi slovo "k"

contains_char = df['Athlete(s) with the most medals\n(gold–silver–bronze)'].str.contains('k')
print(df[contains_char][['Discipline','Athlete(s) with the most medals\n(gold–silver–bronze)']])
print('')



# 18. Dodaj kolonu Discipline name length sa brojem karaktera:

df['Discipline name length'] = df['Discipline'].apply(lambda x: len(x))
print(df[['Discipline','Discipline name length']])
print('')


# 19. Ako disciplina ima vise zlatnih nego srebrnih + bronzanih, stavi True, inace False


df['Has Gold Dominance'] = df.apply(lambda row: row['Gold medals awarded'] > (row['Silver medals awarded'] + row['Bronze medals awarded']), axis=1)
print(df['Has Gold Dominance'])
print('')


# 20. Dodaj kolonu Top athlete only koja uzima samo prvo ime iz kolone 'Athlete(s) with the most medals\n(gold–silver–bronze)'


df['Top athlete'] = df['Athlete(s) with the most medals\n(gold–silver–bronze)'].apply(lambda x: x.split('(')[0].strip())
print(df['Top athlete'])
print('')


# 21. Dodaj kolonu Medal Level:
# - 'Low' ako je < 50 medalja
# - 'Medium' ako je 50–150
# - 'High' ako je >150

df['Medal Level'] = df['Total medals awarded'].apply(lambda x:
    'Low' if x < 50 else ('Medium' if x <= 150 else 'High')
)
print(df[['Medal Level','Total medals awarded']])

df.to_csv('osvajaci_najvise_medalja_po_sportovima.csv', index =False)

print(df)


