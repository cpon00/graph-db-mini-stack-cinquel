from datetime import date
import csv
import json
import os
import sys
# from neo4j import GraphDatabase

# For simplicity, we assume that the program runs where the files are located.
MOVIE_SOURCE = 'tmdb_5000_movies.csv'
CREDIT_SOURCE = 'tmdb_5000_credits.csv'

MOVIES = 'movies.csv'
GENRES = 'genres.csv'
KEYWORDS = 'keywords.csv'
CAST = 'cast.csv'
CREW = 'crew.csv'
# Writes into destination
MOVIES = open(MOVIES, 'w')

# to connect to database
# db_user = os.environ['DB_USER'] if os.environ.get('DB_USER') else 'neo4j'


# # The Neo4j documentation calls this object `driver` but the name `db` is used here
# # to provide an analogy across various DAL examples.
# db = GraphDatabase.driver(os.environ['DB_URL'], auth=(db_user, os.environ['DB_PASSWORD']))

# We have two files to load, but only some of the files in the credits are relevant.
# So we open both and use only the cast and crew portion of credits.

with open(MOVIE_SOURCE, 'r+', encoding='UTF-8') as m:
    movie_list = list(csv.DictReader(m))
    for movie in movie_list:
        result = {}
        result['id'] = int(movie['id'])
        result['title'] = movie['title']
        # There were singular movies in our dataset that had bad values. As such, rather than simply removing them, we gave them an arbitrary date.
        if movie['release_date'] == '':
            result['release_date'] = date.fromisoformat('3000-1-1')
        else:
            result['release_date'] = date.fromisoformat(
                movie['release_date'])
        result['original_language'] = movie['original_language']
        result['budget'] = int(movie['budget'])

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

        # result['cast'] = json.loads(credit['cast'])
        # result['crew'] = json.loads(credit['crew'])
        MOVIES.write(f"{result['id']}|{result['title']}|{result['release_date']}|{result['original_language']}|" \
                                  f"{result['budget']}|{result['popularity']}|{result['vote_average']}|{result['runtime']}\n")

MOVIES.close()

# Print statement for ID of inserted entry.
# print(x.inserted_id)