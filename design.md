# Populating the Database

## This process assumes you have already gotten a fresh neo4j database running on your machine

1. Run loader.py
2. run:

```
NEO4J_CONF=<PATH TO CONF> neo4j-admin import --database=neo4j --delimiter="|" --nodes=Movie=<PATH TO movies.csv> --nodes=Genre=<PATH TO genres.csv> --nodes=Cast=<PATH TO cast.csv> --nodes=Crew=<PATH TO crew.csv> —nodes=Keywords=<PATH TO keywords.csv> --relationships=<PATH TO genre_relations.csv> --relationships=<PATH TO cast_relations.csv> --relationships=<PATH TO keyword_relations.csv> --relationships=<PATH TO crew_relations.csv>
```

3. start your, now populated, neo4j server with this command:

```
NEO4J_CONF=<PATH TO CONF> neo4j console
```
