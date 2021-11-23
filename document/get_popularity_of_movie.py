import sys

from tmdb5000_dal import get_popularity_of_movie

if len(sys.argv) != 2:
    print('Usage: search_by_title <query>')
    exit(1)

query = sys.argv[1]
result = get_popularity_of_movie(query)
print(result)
