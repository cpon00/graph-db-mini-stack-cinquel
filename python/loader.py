from datetime import date
import csv
import json

# For simplicity, we assume that the program runs where the files are located.
MOVIE_SOURCE = 'tmdb_5000_movies.csv'
CREDIT_SOURCE = 'tmdb_5000_credits.csv'

# CSVs to represent nodes.
MOVIES = 'movies.csv'
GENRES = 'genres.csv'
KEYWORDS = 'keywords.csv'
CAST = 'cast.csv'
CREW = 'crew.csv'


# CSVs to represent node relationships.
GENRE_RELATIONS = 'genre_relations.csv'
KEYWORD_RELATIONS = 'keyword_relations.csv'
CAST_RELATIONS = 'cast_relations.csv'
CREW_RELATIONS = 'crew_relations.csv'

# For simplicity, we were able to contain all node creation and relationships within one python file.
processed_movies = open(MOVIES, 'w+')
processed_genres = open(GENRES, 'w+')
processed_keywords = open(KEYWORDS, 'w+')
processed_cast = open(CAST, 'w+')
processed_crew = open (CREW, "w+")
processed_genre_relations = open(GENRE_RELATIONS, 'w+')
processed_keyword_relations = open(KEYWORD_RELATIONS, 'w+')
processed_cast_relations = open(CAST_RELATIONS, 'w+')
processed_crew_relations = open(CREW_RELATIONS, 'w+')

# These data structures will represent the non-unique genres and keywords. As such, they are contained in a set.
genres = set()
keywords = set()
cast = set()
crew = set()

# To avoid the issue of commas, we simply specified the delimiter '|' in the import command.

# For further simplicity, we populated the headers of the node files and their relationships before writing the data to the files.
processed_movies.write(f'movieId:id(Movie)|title:STRING|release_date:DATE|original_language:STRING|budget:INT|popularity:FLOAT|vote_average:FLOAT|runtime:INT\n')

processed_genres.write(f'genreID:ID(Genre)\n')
processed_genre_relations.write(f':START_ID(Movie)|:END_ID(Genre)|:TYPE\n')

processed_keywords.write(f'keywordID:ID(Keyword)\n')
processed_keyword_relations.write(f':START_ID(Movie)|:END_ID(Keyword)|:TYPE\n')

processed_cast.write(f'castID:ID(Cast)\n')
processed_cast_relations.write(f':START_ID(Cast)|:END_ID(Movie)|role:STRING|:TYPE\n')

processed_crew.write(f'crewID:ID(Crew)\n')
processed_crew_relations.write(f':START_ID(Crew)|:END_ID(Movie)|job:STRING|:TYPE\n')

# Opening and reading files:
with open(MOVIE_SOURCE, 'r+', encoding='UTF-8') as m, open(CREDIT_SOURCE, 'r+', encoding='UTF-8') as c:
    movie_list, credit_list = list(csv.DictReader(m)), list(csv.DictReader(c))
    for movie, credit in zip(movie_list, credit_list):
        result = {}
        result['id'] = int(movie['id'])
        result['title'] = movie['title']
        # There were singular movies in our dataset that had bad values. As such, rather than simply removing them, we gave them an arbitrary date.
        if movie['release_date'] == '':
            result['release_date'] = date.fromisoformat("1000-01-01")
        else:
            result['release_date'] = date.fromisoformat(movie['release_date'])
        result['original_language'] = movie['original_language']
        result['budget'] = int(movie['budget'])
        result['popularity'] = float(movie['popularity'])
        result['vote_average'] = float(movie['vote_average'])
        # Likewise as above.
        if movie['runtime'] == '':
            result['runtime'] = 0
        else:
            result['runtime'] = int(float(movie['runtime']))

        # The genres, keywords, cast, and crew data is all in the form of a json snippet. As such, I processed the data into a dictionary, then added those entities and their relationships.
        for entry in json.loads(movie['genres']): 
            genres.add(entry['name'])
            processed_genre_relations.write(f"{result['id']}|{entry['name']}|CLASSIFIED_AS\n")
            
        for entry in json.loads(movie['keywords']): 
            keywords.add(entry['name'])
            processed_keyword_relations.write(f"{result['id']}|{entry['name']}|HAS_KEYWORD\n")
        
        for entry in json.loads(credit['cast']):
            name = entry['name'].replace('"', "'").replace('|', '/')
            character = entry['character'].replace('"', "'").replace('|', '/')
            cast.add(name)
            processed_cast_relations.write(f"{name}|{result['id']}|{character}|PERFORMED IN\n")
            
            
        for entry in json.loads(credit['crew']):
            name = entry['name'].replace('"', "'").replace('|', '/')
            job = entry['job'].replace('"', "'").replace('|', '/')
            crew.add(name)
            processed_crew_relations.write(f"{name}|{result['id']}|{job}|WORKED ON\n")
        
        # Final write statement for movies.
        processed_movies.write(f"{result['id']}|{result['title']}|{result['release_date']}|{result['original_language']}|" \
                                  f"{result['budget']}|{result['popularity']}|{result['vote_average']}|{result['runtime']}\n")

# Populating genres and keywords. As iterated above, they are non-distinct.
for key in genres:
    processed_genres.write(f"{key}\n")

for key in keywords:
    processed_keywords.write(f"{key}\n")
    
for key in cast:
    processed_cast.write(f"{key}\n")
    
for key in crew:
    processed_crew.write(f"{key}\n")

processed_movies.close()
processed_keywords.close()
processed_genres.close()
processed_crew.close()
processed_cast.close()

