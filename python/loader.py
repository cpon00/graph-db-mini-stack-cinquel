from datetime import datetime
import csv
import json
import os
# from neo4j import GraphDatabase

# For simplicity, we assume that the program runs where the files are located.
MOVIE_SOURCE = 'tmdb_5000_movies.csv'
CREDIT_SOURCE = 'tmdb_5000_credits.csv'

DESTINATION = 'movies.csv'
# Writes into destination
post_processed_file = open(DESTINATION, 'w')
current_movie_id = None

# to connect to database
# db_user = os.environ['DB_USER'] if os.environ.get('DB_USER') else 'neo4j'


# # The Neo4j documentation calls this object `driver` but the name `db` is used here
# # to provide an analogy across various DAL examples.
# db = GraphDatabase.driver(os.environ['DB_URL'], auth=(db_user, os.environ['DB_PASSWORD']))

# We have two files to load, but only some of the files in the credits are relevant.
# So we open both and use only the cast and crew portion of credits.

with open(MOVIE_SOURCE, 'r+', encoding='UTF-8') as m, open(CREDIT_SOURCE, 'r+', encoding='UTF-8') as c:
    movie_list, credit_list = list(csv.DictReader(m)), list(csv.DictReader(c))
    for movie, credit in zip(movie_list, credit_list):

        result = {}
        result['id'] = int(movie['id'])
        result['title'] = movie['title']
        # There were singular movies in our dataset that had bad values. As such, rather than simply removing them, we gave them an arbitrary date.
        if movie['release_date'] == '':
            result['release_date'] = datetime.strptime('3000-1-1', '%Y-%m-%d')
        else:
            result['release_date'] = datetime.strptime(
                movie['release_date'], '%Y-%m-%d')
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
        # Instead of creating a results object, I could have built an object within the insert_one(), but I felt this was clearer and more concise. Pardon my space usage.
        # x = db.movie.insert_one(result)

        print(result['id'], result['title'], result['release_date'],
              result['original_language'], result['budget'], result['popularity'], result['vote_average'], result['runtime'], sep='|')

# post_processed_file.close()

# Print statement for ID of inserted entry.
# print(x.inserted_id)
