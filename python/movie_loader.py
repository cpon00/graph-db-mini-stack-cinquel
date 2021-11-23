from datetime import date
import csv
import json
import os
import sys

# For simplicity, we assume that the program runs where the files are located.
MOVIE_SOURCE = 'tmdb_5000_movies.csv'
CREDIT_SOURCE = 'tmdb_5000_credits.csv'

MOVIES = 'movies.csv'
GENRES = 'genres.csv'
KEYWORDS = 'keywords.csv'
CAST = 'cast.csv'
CREW = 'crew.csv'

GENRE_RELATIONS = 'genre_relations.csv'
KEYWORD_RELATIONS = 'keyword_relations.csv'
# Writes into destination
processed_movies = open(MOVIES, 'w+')
processed_genres = open(GENRES, 'w+')
processed_keywords = open(KEYWORDS, 'w+')
processed_cast = open(CAST, 'w+')
processed_crew = open (CREW, "w+")
processed_genre_relations = open(GENRE_RELATIONS, 'w+')
processed_keyword_relations = open(KEYWORD_RELATIONS, 'w+')
processed_cast_relations = open(GENRE_RELATIONS, 'w+')
processed_crew_relations = open(GENRE_RELATIONS, 'w+')
# to connect to database
# db_user = os.environ['DB_USER'] if os.environ.get('DB_USER') else 'neo4j'


# # The Neo4j documentation calls this object `driver` but the name `db` is used here
# # to provide an analogy across various DAL examples.
# db = GraphDatabase.driver(os.environ['DB_URL'], auth=(db_user, os.environ['DB_PASSWORD']))

# We have two files to load, but only some of the files in the credits are relevant.
# So we open both and use only the cast and crew portion of credits.

# genre_dict = {}
# for genres in movies.genres:
#     for item in genres:
#         genre_id = item['id']
#         genre_name = item['name']
#         genre_dict[genre_id] = genre_name
        
# kw_dict = {}
# for (id, keywords) in zip(movies.id, movies.keywords):
#     for kw in keywords:
#         kw_id = kw['id']
#         kw_name = kw['name']
#         kw_dict[kw_id] = kw_name

# for (key, value) in kw_dict.items():
#     value = value.replace("'", "''")
#     print(f'INSERT INTO keyword VALUES({key}, \'{value}\');'
#           )
genres = set()
keywords = set()
cast = set()
crew = set()
processed_movies.write(f'movieId:id(Movie)|title:STRING|release_date:DATE|original_language:STRING|budget:INT|popularity:FLOAT|vote_average:FLOAT|runtime:INT\n')

processed_genres.write(f'genreID:ID(Genre)\n')
processed_genre_relations.write(f':START_ID(Movie)|:END_ID(Genre)|:TYPE\n')

processed_keywords.write(f'keywordID:ID(Keyword)\n')
processed_keyword_relations.write(f':START_ID(Movie)|:END_ID(Keyword)|:TYPE\n')

processed_cast.write(f'castID:ID(Actor)|role:STRING\n')
processed_cast_relations.write(f':START_ID(Movie)|:END_ID(Actor)|:TYPE\n')

processed_crew.write(f'crewID:ID(Crew)|job:STRING\n')
processed_crew_relations.write(f':START_ID(Movie)|:END_ID(Crew)|:TYPE\n')


with open(MOVIE_SOURCE, 'r+', encoding='UTF-8') as m, open(CREDIT_SOURCE, 'r+', encoding='UTF-8') as c:
    movie_list, credit_list = list(csv.DictReader(m)), list(csv.DictReader(c))
    for movie, credit in zip(movie_list, credit_list):
        result = {}
        result['id'] = int(movie['id'])
        result['title'] = movie['title']
        # There were singular movies in our dataset that had bad values. As such, rather than simply removing them, we gave them an arbitrary date.
        if movie['release_date'] == '':
            result['release_date'] = date.fromisoformat("1000-01-01")
        else:
            result['release_date'] = date.fromisoformat(movie['release_date'])
        result['original_language'] = movie['original_language']
        result['budget'] = int(movie['budget'])

        for entry in json.loads(movie['genres']): 
            genres.add(entry['name'])
            processed_genre_relations.write(f"{result['id']}|{entry['name']}|CLASSIFIED_AS\n")
        for entry in json.loads(movie['keywords']): 
            keywords.add(entry['name'])
            processed_keyword_relations.write(f"{result['id']}|{entry['name']}|HAS_KEYWORD\n")
        # result['genre'] = json.loads(movie['genres'])
        # result['keywords'] = json.loads(movie['keywords'])
        # result['overview'] = movie['overview']

        result['popularity'] = float(movie['popularity'])
        result['vote_average'] = float(movie['vote_average'])

        # Likewise as above.
        if movie['runtime'] == '':
            result['runtime'] = 0
        else:
            result['runtime'] = int(float(movie['runtime']))

        for entry in json.loads(credit['cast']):
            processed_cast.write(f"{entry['name']}|{entry['character']}\n")
            processed_cast_relations.write(f"{result['id']}|{entry['name']}|PERFORMED IN\n")
            
        for entry in json.loads(credit['crew']):
            processed_crew.write(f"{entry['name']}|{entry['job']}\n")
            processed_crew_relations.write(f"{result['id']}|{entry['name']}|WORKED ON\n")
        
        # POPULATION STATEMENTS
        processed_movies.write(f"{result['id']}|{result['title']}|{result['release_date']}|{result['original_language']}|" \
                                  f"{result['budget']}|{result['popularity']}|{result['vote_average']}|{result['runtime']}\n")
        
        # DEBUGGING STATEMENTS
        # print(f"{result['id']}|{result['title']}|{result['release_date']}|{result['original_language']}|" \
        #                           f"{result['budget']}|{result['popularity']}|{result['vote_average']}|{result['runtime']}\n")

for key in genres:
    processed_genres.write(f"{key}\n")

for key in keywords:
    processed_keywords.write(f"{key}\n")

processed_movies.close()
processed_keywords.close()
processed_genres.close()
processed_crew.close()
processed_cast.close()

# Print statement for ID of inserted entry.
# print(x.inserted_id)
