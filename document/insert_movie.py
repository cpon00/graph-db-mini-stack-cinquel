import sys

from tmdb5000_dal import insert_movie

if len(sys.argv) != 7:
    print('Usage: add_movie <original language> <title> <popularity> <date> <vote average> <vote count>')
    exit(1)

original_language = sys.argv[1]
title = sys.argv[2]
popularity = sys.argv[3]
release_date = sys.argv[4]
vote_average = sys.argv[5]
vote_count = sys.argv[6]

try:
    movie = insert_movie(original_language, title,
                         popularity, release_date, vote_average, vote_count)
    print(
        f'Movie “{movie.title}” ({movie.release_date}) added with ID {movie.id}.')
except ValueError:
    print(f'Sorry, something went wrong. Please double-check inputted values.')
