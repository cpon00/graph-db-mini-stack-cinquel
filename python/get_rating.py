import sys
from tmdb_dal import getAverageRating

if len(sys.argv) != 2:
    print('Usage: remove_movie <movieId>')
    exit(1)


movieId = sys.argv[1]

try:
    result = getAverageRating(int(movieId))
    print(
        f"{movieId} has an average rating of {result}")
except ValueError:
    print(
        f'Sorry, something went wrong.')
