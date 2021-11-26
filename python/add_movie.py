import sys


from tmdb_dal import insert_movie

if len(sys.argv) != 9:
    print('Usage: add_movie <budget> <movieId> <orgininal_language> <popularity> <release_date> <runtime> <title> <vote_average>')
    exit(1)


budget = sys.argv[1]
movieId = sys.argv[2]
original_language = sys.argv[3]
popularity = sys.argv[4]
release_date = sys.argv[5]
runtime = sys.argv[6]
title = sys.argv[7]
vote_average = sys.argv[8]


try:
    movie = insert_movie(int(budget), int(movieId), original_language, float(
        popularity), release_date, int(runtime), title, float(vote_average))
    print(
        f"Movie “{movie.get('title')}” added with id {movieId} ")
except ValueError:
    print(
        f'Sorry, something went wrong.')
