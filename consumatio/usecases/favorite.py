def set_favorite(tmdb: object, database: object, external_id: str, media: str,
                 code: int, seasonNumber: int, episodeNumber: int,
                 favorite: bool) -> dict:
    """
    :param tmdb: <object> TMDB object to make API requests
    :param database: <object> Database object to access database
    :param external_id: <str> External Id provided by OAuth
    :param media: <str> Type of media to
    :param code: <int> Code of the media to favorite
    :param seasonNumber: <int> Number of season if media is season
    :param episodeNumber: <int> Number of episode if media is episode
    :param favorite: <bool> Boolean to set favorite to
    :return: <dict> Successful response
    """
    user_id = 0

    if not database.user_exists(external_id):
        database.user(external_id)
    user_id = database.get_user_id(external_id)

    if media == "Season":
        code = tmdb.get_season_details(code, seasonNumber).get("code")

    if media == "Episode":
        code = tmdb.get_episode_details(code, seasonNumber,
                                        episodeNumber).get("code")

    if not database.media_data_exists(user_id, media, code):
        database.media_Data(user_id, media, code)

    database.favorite(user_id, media, code, favorite)
    return {"status": True}