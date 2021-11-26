import sys


from tmdb_dal import insert_movie
from tmdb_dal import insert_title

# if len(sys.argv) != 9:
#     print('Usage: add_movie <title> <date> <language> <budget> <popularity> <vote-average> <runtime> <id>')
#     exit(1)


title = sys.argv[1]
print(title)

#"1000-01-01"
# date = sys.argv[2]
# print(date)

# lang = sys.argv[3]
# print(lang)

# budget = sys.argv[4]
# print(budget)

# popularity = sys.argv[5]
# print(popularity)

# vote_av = sys.argv[6]
# print(vote_av)

# runtime = sys.argv[7]
# print(runtime)

# movie_id = sys.argv[8]
# print(movie_id)




# "Josh", "2000-09-17", "en", 10000, 10, 100, 1000

try:
    movie = insert_title(title)
    # movie = insert_movie(title, date, lang, int(budget), float(popularity), float(vote_av), int(runtime), int(movie_id))
    print(
        f"Movie “{movie.get('title')}” added with")
except ValueError:
    print(
        f'Sorry, something went wrong.')


# movieId:id(Movie)|title:STRING|release_date:DATE|original_language:STRING|budget:INT|popularity:FLOAT|vote_average:FLOAT|runtime:INT
