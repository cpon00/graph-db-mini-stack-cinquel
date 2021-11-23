import sys

from tmdb5000_dal import remove_movie

if len(sys.argv) != 2:
    print('Usage: remove_movie <id>')
    exit(1)

movie_to_remove = sys.argv[1]

try:
    remove_movie(movie_to_remove)
except ValueError:
    print(f'Sorry, something went wrong. Please double-check inputted id')
