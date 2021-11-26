import sys
from tmdb_dal import remove_movie

if len(sys.argv) != 2:
    print('Usage: remove_movie <movieId>')
    exit(1)


movieId = sys.argv[1]

try:
    movie = remove_movie(int(movieId))
    print(
        f"Movie with ID:{movieId} has been removed")
except ValueError:
    print(
        f'Sorry, something went wrong.')
