import { insertMovie } from './netflix-dal.mjs'

if (process.argv.length !== 11) {
  console.log('Usage: add-movie <title> <release_day> <release_month> <release_year> <language> <budget> <popularity> <vote_average> <runtime>')
  process.exit(1)
}


const title = process.argv[2]
const date = new Date(process.argv[5], proceprocess.argv[4], process.argv[3])
const language = process.argv[6]
const budget = process.argv[7]
const popularity = process.argv[8]
const vote_average = process.argv[9]
const runtime = process.argv[10]

try {
  const movieNode = await insertMovie(title, date, language, budget, popularity, vote_average, runtime)
  const { properties: movie } = movieNode
  console.log(`Movie “${movie.title}” added with ID ${movieNode.identity}.`)
} catch (error) {
  console.error(`Sorry, something went wrong. Please ensure that “${year}” is a valid year.`)
}

// Explicitly exit sync since we are asynchronous at this point.
process.exit(0)