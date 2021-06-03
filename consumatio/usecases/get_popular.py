def get_popular(external_id: str, tmdb: object, type: str, country: str,
                page: int) -> dict:
    """
    Get popular Movies/TV Shows for a provided country
    :param external_id: <str> External ID provided by OAuth 
    :param tmdb: <object> Tmdb object
    :param type: <str> Popular item type "movie" or "tv"
    :param country: <str> Country code (uppercase) currently only applicable for movies
    :param page: <int> Search page (minimum:1 maximum:1000)
    :return: <dict> popular media
    """
    dict = {}
    if type == "Movie":
        dict_movie_results = tmdb.get_popular_movies(country, external_id,
                                                     page)
        dict = {
            "total_pages": dict_movie_results.get("total_pages"),
            "results": dict_movie_results.get("results")
        }

    elif type == "TV":
        dict_tv_results = tmdb.get_popular_tv(external_id, page)
        dict = {
            "total_pages": dict_tv_results.get("total_pages"),
            "results": dict_tv_results.get("results")
        }

    return dict
