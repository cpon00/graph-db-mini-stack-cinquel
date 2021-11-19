# Netflix Practice

## Queries

### Create new nodes and relationships: Do some IMDB/Wikipedia research on your choice of artists (performers, directors, writers, musicians, etc.) who are affiliated with movies/shows in the Netflix dataset and connect them to those shows’ nodes with appropriate relationships. Pick a mix—around five (5) such nodes will be good, and make sure they have movies/shows in common, in different combinations. Research and define a small set of common properties for those artists, such as gender, birthdate, nationality, etc. Show the MATCH/CREATE/RETURN clauses that make these additions and a culminating query that produces a graph showing all of your additions and the movies/shows that they worked on (but no ratings—that would be too much).

```json
db.movies.find( {title: /spongebob/i}, { _id: 0, id: 1, title: 1, year: 1}).sort({title: 1})
```

<center><img src="./assets/q1.png" style="width: 90%" ></img></center>

### Viewers who are fans: Let’s define a “fan” as someone who has rated a movie/show with a 5. Formulate a query that graphs the viewers who have given a 5 rating to the work of one of your selected artists. Make sure to return the viewers, the movies/shows that they rated, your chosen artist, and what they did in those movies/shows.

```json
db.movies.aggregate([
  {"$match" : {title: /spongebob/i}},
  {"$group" : {_id:"$year", count:{$sum:1}}},
  {"$sort":{year: 1}}
])
```

<center><img src="./assets/q2.png" style="width: 90%" ></img></center>

### Love/hate relationship: Pick two movies that are likely to have a decent overlap of viewers. Formulate a query that graphs the viewers who hated one movie (rated it a 1) but loved the other (rated it a 5).

```json
db.movies.aggregate([
  {"$match" : {title: /dog/i}},
  {"$group" : {_id:"$year", count:{$sum:1}}},
  {"$sort": {count: -1, _id: 1}},
  {"$limit": 5}
])
```

<center><img src="./assets/q3.png" style="width: 90%" ></img></center>

### Watch party 1: Define a set of criteria that filters out a small subset of movies/shows (no more than 3 to be safe). Formulate a query that produces a graph showing viewers who rated those movies/shows on the same day.

```json
db.movies.aggregate([
  { $unwind: "$ratings" },
  { $match: { $and:[ { 'ratings.viewer_id': 2442 }, { 'ratings.rating': 5 } ] } },
  { $group: {_id: {title: '$title', year: '$year'} }},
  { $sort:  {'_id.title': 1}},
])
```

<center><img src="./assets/q4.png" style="width: 90%" ></img></center>

### Watch party 2: Define a set of criteria that filters out a small subset of the artists that you’ve loaded into Neo4j. Formulate a query that produces a graph showing viewers who rated a movie/show on the same day, for movies/shows that your chosen artists worked on. Make sure to return the viewers, the movies/shows that they rated, the chosen artists, and what they did in those movies/shows.

```json
db.movies.aggregate([
  { $unwind: "$ratings"},
  {"$match" : {title: /spongebob/i}},
  {"$group" : {_id:{title: "$title", year: "$year"}, avg_rating: {$avg:"$ratings.rating"}}},
  {"$sort" :  {avg_rating: -1, title: 1}}
])
```

<center><img src="./assets/q5.png" style="width: 90%" ></img></center>
