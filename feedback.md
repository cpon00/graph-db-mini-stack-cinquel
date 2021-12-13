

## Cinquel

##### https://github.com/lmu-cmsi3520-fall2021/graph-db-mini-stack-cinquel

| Category | Feedback | Points |
| --- | --- | ---: |
| _netflix-practice.md_ |  | /25 |
| _.gitignore_ |  |  |
| _schema.pdf/md_ and/or mappings | Schema is communicated clearly and according to the notation used by Neo4j | 5/5 |
| Loader programs | • Preprocesser _loader.py_ appears to run without issues<br><br>• Import appears to run without issues: `121071 nodes 284192 relationships 389847 properties` | 15/15 |
| _design.md_ | _design.md_ doesn’t have any commentary on the choices made for the schema (–2), but it does have sufficient instructions on how to set things up | 3/5 |
| _queries.md_ |  | /25 |
| DAL module | | |
| • Configuration/setup | Configuration code uses library correctly and properly separates configuration information as an environment variable | 5/5 |
| • Retrieval | `getAverageRating` successfully performs its intended query but, because it returns a single number, it does not meet the criterion of “return a graph matching those arguments” at all. A query that better exemplifies graph database use could have been chosen (–2) | 2/7 |
| • CUD | `insert_movie` and `remove_movie` successfully perform their expected database modifications—but it would be nice if `remove_movie` actually returned its result, so that the caller has a sense of how that query operation went (–1) | 9/7 |
| DAL programs | • _get_rating.py_ checks the argument count, provides help when needed, and displays readable results. However, it sends the movie ID to the DAL function as an integer when it should actually be the _string_ version of that integer (don’t look at me—that’s how your import instructions loaded the dataset!). Further, it shows a scary stack trace when no results are found<br><br>• _add_movie.py_ checks the argument count, provides help when needed, and displays readable results. It enforces data types as well. However it shows the same type discrepancy as _get_rating.py_ in that it models `movieId` as an integer when the database models it as a string. This would make duplicate-checking a tad more problematic (if the underlying DAL function did it)<br><br>• Ditto _remove_movie.py_—it’s got the same characteristics including the out-of-sync `movieId` typing<br><br>The universal type mismatch hints to me that there was some miscommunication between the data loader and DAL program folks. Either way, it’s an overall defect and so we’ll apply an overall deduction to it (–2) | 4/6 |
| Code maintainability |  |  |
| Code readability |  |  |
| Version control |  |  |
| Punctuality |  |  |
| | **Total** | **43/50** so far |
