from operator import and_
import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Float, ForeignKey, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

db = create_engine(os.environ['DB_URL'])
metadata = MetaData(db)
movie_table = Table('movie', metadata, autoload=True)
genre_table = Table('genre', metadata, autoload=True)
movie_genre_table = Table('moviegenre', metadata, autoload=True)
actor_table = Table('actor', metadata, autoload=True)
character_table = Table('character', metadata, autoload=True)
keyword_table = Table('keyword', metadata, autoload=True)
movie_keyword_table = Table('moviekeyword', metadata, autoload=True)

# Raw SQL-style implementation of a movie query.


def search_movies_by_title(query):
    with db.connect() as connection:
        # We want actual %'s so need to escape them in the string.
        result_set = connection.execute(f"""
            SELECT movie.title, movie.release_date FROM movie WHERE title ILIKE '%%{query}%%' ORDER BY title
        """)
        result = result_set.fetchall()
        return list(result)


def get_popularity_of_movie(movie_id):
    with db.connect() as connection:
        statement = select(movie_table.c.popularity).where(
            movie_table.c.id == movie_id)
        result_set = connection.execute(statement)
        return result_set.fetchone()[0]

# ORM-style implementation of a movie inserter.


def insert_movie(original_language, title, popularity, release_date, vote_average, vote_count):
    movie = Movie(original_language=original_language, title=title, popularity=popularity,
                  release_date=release_date, vote_average=vote_average, vote_count=vote_count)
    current_session.add(movie)
    current_session.commit()  # Make the change permanent.
    return movie


def remove_movie(movie_id):
    with db.connect() as connection:
        connection.execute(movie_table.delete().where(
            movie_table.c.id == movie_id))
        current_session.commit()
        return 0


# def actor_works(term):
#     with db.connect() as connection:
#         statement = select(movie_table.c).where(
#             movie_table.c.title.find(term)
#         )
#         result_set = connection.execute(statement)
#         result = result_set.fetchall()
#         return list(result)
# SQL builder-style implementation of an aggregate query.
# def get_average_rating_of_movie(movie_id):
#     with db.connect() as connection:
#         statement = select([func.avg(rating_table.c.rating)]).where(rating_table.c.movie_id == movie_id)
#         result_set = connection.execute(statement)

#         # We know in advance that this will be a single row with a single column so we feel safe about hardcoding this.
#         # A non-existent movie will yield `None` for this expression.
#         return result_set.fetchone()[0]


# For ORM-style implementations, we need to define a few things first.
ORM_Base = declarative_base()

# 3original_language, title, popularity, release_date, runtime, vote_average, vote_count


class Movie(ORM_Base):
    __tablename__ = 'movie'
    id = Column(Integer, Sequence('movie_id_seq'), primary_key=True)
    original_language = Column(String)
    title = Column(String)
    popularity = Column(Float)
    release_date = Column(Date)
    vote_average = Column(Float)
    vote_count = Column(Integer)


class Genre(ORM_Base):
    __tablename__ = 'genre'
    genre_id = Column(Integer, Sequence('genre_id_seq'), primary_key=True)
    genre_name = Column(Integer)


class MovieGenre(ORM_Base):
    __tablename__ = 'moviegenre'
    movie_id = Column(Integer, ForeignKey('movie.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genre.genre_id'))


class Actor(ORM_Base):
    __tablename__ = 'actor'
    id = Column(Integer, Sequence('movie_id_seq'), primary_key=True)
    name = Column(String)


class Character(ORM_Base):
    __tablename__ = 'character'
    movie_id = Column(Integer, ForeignKey('movie.id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('actor.id'))
    character_name = Column(String)
    gender = Column(Integer)


class Keyword(ORM_Base):
    __tablename__ = 'keyword'
    keyword_id = Column(Integer, Sequence('keyword_id_seq'), primary_key=True)
    keyword_name = Column(String)


class MovieKeyword(ORM_Base):
    __tablename__ = 'moviekeyword'
    movie_id = Column(Integer, Sequence('movie_id_seq'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keyword.id'))


# The notion of a Session is a multifaceted one whose usage and implementation may change depending on the type
# of application that is using this DAL (particularly, a standalone application vs. a web service). It is implemented
# here in the simplest possible way. Note that if this DAL is to be used in other contexts, code surrounding sessions
# may have to change.
#
# At a minimum, we follow the basic SQLAlchemy rule that sessions should be external to the functions that use them.
# Thus, we define current_session at this upper level, and not within each function.
Session = sessionmaker(bind=db)
current_session = Session()
