import json
import pandas as pd


def formatter(path):
    df = pd.read_csv(path)
    df['release_date'] = pd.to_datetime(
        df['release_date']).apply(lambda x: x.date())
    json_columns = ['genres', 'keywords', 'production_countries',
                    'production_companies', 'spoken_languages']
    for column in json_columns:
        df[column] = df[column].apply(json.loads)
    return df


movies = formatter("./tmdb_5000_movies.csv")

for (id, original_language, title, popularity, release_date, runtime, vote_average, vote_count) in zip(movies.id, movies.original_language, movies.title, movies.popularity, movies.release_date, movies.runtime, movies.vote_average, movies.vote_count):
    id = int(float(id)) if id != '' else None
    if not id:
        continue
    vote_count = int(float(vote_count))
    title = title.replace("'", "''")
    print(
        f'INSERT INTO movie VALUES({id}, \'{original_language}\', \'{title}\', {popularity}, \'{release_date}\', {vote_average}, {vote_count});')

print('SELECT setval(\'movie_id_seq\', (SELECT MAX(id) from movie));')

genre_dict = {}
for genres in movies.genres:
    for item in genres:
        genre_id = item['id']
        genre_name = item['name']
        genre_dict[genre_id] = genre_name

for (key, value) in genre_dict.items():
    print(f'INSERT INTO genre VALUES({key}, \'{value}\');')

for (id, genres) in zip(movies.id, movies.genres):
    for item in genres:
        genre_id = item['id']
        print(f'INSERT INTO moviegenre VALUES({id}, {genre_id});')

kw_dict = {}
for (id, keywords) in zip(movies.id, movies.keywords):
    for kw in keywords:
        kw_id = kw['id']
        kw_name = kw['name']
        kw_dict[kw_id] = kw_name

for (key, value) in kw_dict.items():
    value = value.replace("'", "''")
    print(f'INSERT INTO keyword VALUES({key}, \'{value}\');'
          )

for (id, keywords) in zip(movies.id, movies.keywords):
    for kw in keywords:
        kw_id = kw['id']
        print(f'INSERT INTO moviekeyword VALUES({id}, {kw_id});')
