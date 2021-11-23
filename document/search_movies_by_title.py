import sys

from tmdb5000_dal import search_movies_by_title
if len(sys.argv) != 2:
    print('Usage: search_movies_by_title <id>')
    exit(1)


query = sys.argv[1]
result = search_movies_by_title(query)

for movie in result:
    print(movie)
