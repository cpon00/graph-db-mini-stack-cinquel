import os
from neo4j import GraphDatabase

# This is for convenience since the `neo4j` user is known to be created by default.
# We do still let an environment variable override it if needed.
db_user = os.environ['DB_USER'] if os.environ.get('DB_USER') else 'neo4j'

# The Neo4j documentation calls this object `driver` but the name `db` is used here
# to provide an analogy across various DAL examples.
db = GraphDatabase.driver(os.environ['DB_URL'], auth=(
    db_user, os.environ['DB_PASSWORD']))


def insert_movie(budget, movieId, original_language, popularity, release_date, runtime, title, vote_average):
    with db.session() as session:
        result = session.run(
            """
            CREATE (insertedMovie:Movie { budget: $budget, movieId: $movieId, original_language: $original_language, popularity: $popularity, release_date: $release_date, runtime:$runtime, title: $title, vote_average: $vote_average})
            RETURN insertedMovie
            """,
            budget=budget,
            movieId=movieId,
            title=title,
            release_date=release_date,
            original_language=original_language,
            popularity=popularity,
            vote_average=vote_average,
            runtime=runtime
        )

        # This returns the full node so we have its identity and labels.
        return result.single().get('insertedMovie')


def remove_movie(movieId):
    with db.session() as session:
        result = session.run(
            """
            MATCH (removedMovie:Movie { movieId: $movieId})
            DELETE removedMovie
            """,
            movieId=movieId,
        )

# from netflix


def getAverageRating(movieId):
    with db.session() as session:
        result = session.run(
            """
            MATCH (m:Movie {movieId: $movieId})
            RETURN m.vote_average
            """,
            movieId=movieId,
        )
        return result.single().get('m.vote_average')
