from ariadne import ObjectType, QueryType, gql, make_executable_schema, graphql_sync
from consumatio.external.tmdb import Tmdb
from consumatio.usecases.movie_details import *
from consumatio.usecases.tv_details import *
from consumatio.usecases.season_details import *
from consumatio.usecases.episode_details import *
from consumatio.usecases.search_details import *
from flask import Flask, request, jsonify
from flask_cors import CORS
from ariadne.constants import PLAYGROUND_HTML
import os

type_defs = gql("""
    type Query {
        movie(code: Int, country: String): Movie!
        tv(code: Int, country: String): TV!
        season(code: Int, seasonNumber: Int): Season!
        episode(code: Int, seasonNumber: Int, episodeNumber: Int): Episode!
        search(str: String): [Result!]
    }
    
    type Search {
        results: [Result]
    }
    
    type Result{
        code: Int
        mediaType: String
        title: String
        overview: String
        releaseDate: String
        posterPath: String
        watchStatus: String
    }

    type Movie {
        code: Int
        title: String
        genres: [Genre]
        overview: String
        popularity: Float
        voteAverage: Float
        releaseDate: String
        runtime: Int
        status: String
        backdrop: String
        poster: String
        providers: [Provider]
        cast: [Cast]
        directors: [Director]
        tmdb: String
        watchStatus: String
        rating: Float
        favorite: Boolean
    }

    type Provider {
        name: String
    }

    type Genre {
        name: String
    }

    type Director {
        name: String
        image: String
    }

    type Cast {
        name: String
        role: String
        image: String
        job: String
    }

    type TV {
        code: Int
        name: String
        genres: [Genre]
        overview: String
        popularity: Float
        voteAverage: Float
        firstAirDate: String
        lastAirDate: String
        status: String
        backdrop: String
        poster: String
        providers: [Provider]
        creators: [Director]
        cast: [Cast]
        numberOfEpisodes: Int
        numberOfSeasons: Int
        tmdb: String
        watchStatus: String
        rating: Float
        favorite: Boolean
    }

    type Season {
        code: Int
        tvCode: Int
        seasonNumber: Int
        name: String
        overview: String
        poster: String
        watchStatus: String
        rating: Float
        favorite: Boolean
    }

    type Episode {
        code: Int
        name: String
        episodeNumber: Int
        seasonNumber: Int
        overview: String
        airDate: String
        voteAverage: Float 
        still: String
        watchStatus: String
        rating: Float
        favorite: Boolean
    }
""")

app = Flask(__name__)
CORS(app)

query = QueryType()


def tmdb_client(api_key=os.getenv('TMDB_KEY')):
    return Tmdb(api_key)


@query.field("movie")
def resolve_movie(*_, code, country):
    tmdb = tmdb_client()
    movie = MovieDetails()
    return movie.get_movie_details(tmdb, code, country)


movie = ObjectType("Movie")


@query.field("tv")
def resolve_tv(*_, code, country):
    tmdb = tmdb_client()
    tv = TVDetails()
    return tv.get_tv_details(tmdb, code, country)


tv = ObjectType("TV")


@query.field("season")
def resolve_season(*_, code, seasonNumber):
    tmdb = tmdb_client()
    season = SeasonDetails()
    return season.get_season_details(tmdb, code, seasonNumber)


season = ObjectType("Season")


@query.field("episode")
def resolve_episode(*_, code, seasonNumber, episodeNumber):
    tmdb = tmdb_client()
    episode = EpisodeDetails()
    return episode.get_episode_details(tmdb, code, seasonNumber, episodeNumber)


episode = ObjectType("Episode")


@query.field("search")
def resolve_search(*_, str):
    tmdb = tmdb_client()
    search = SearchDetails()
    return search.get_search_details(tmdb, str)


search = ObjectType("Search")

schema = make_executable_schema(type_defs, query, movie, tv, season, search)


@app.route("/", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(schema,
                                   data,
                                   context_value=request,
                                   debug=app.debug)

    status_code = 200 if success else 400
    return jsonify(result), status_code


port = int(os.environ['PORT'])

if __name__ == "__main__":
    app.run(debug=True, port=port, host="0.0.0.0")
