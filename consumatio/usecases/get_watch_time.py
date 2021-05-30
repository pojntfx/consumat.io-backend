from consumatio.usecases.get_season import get_season
from consumatio.external.models import *
from consumatio.external.exceptions.invalid_parameter import *


def get_watch_time(tmdb: object, external_id: str, type: str) -> int:
    """
    Get time of watched media of a certain type ("Movie", "TV")
    :param tmdb: <object> TMDB object to make API requests
    :param user: <str> External id of the user
    :param type: <str> Type of the media to get count for (e.g. "Movie", "Season" or "Drama")
    :return: <int> Count of minutes watched of a certain type
    """
    runtime = 0
    if type == 'Movie':
        results = MediaData.query.join(User).filter(
            User.user_id_content == MediaData.user_id_content_media_data,
            MediaData.media_type_content == type,
            User.external_id_content == external_id,
            MediaData.watch_status_content == 'Finished').all()

        for result in results:
            data = tmdb.get_movie_details(result.media_id_content)

            runtime += data.get("runtime")
    elif type == 'TV':
        results = MediaData.query.join(User).filter(
            User.user_id_content == MediaData.user_id_content_media_data,
            MediaData.media_type_content == 'Season',
            User.external_id_content == external_id).all()

        for result in results:
            data = tmdb.get_tv_details(result.tv_code)

            for i in range(1, data.get("number_of_seasons") + 1):
                season = get_season(external_id, tmdb, result.tv_code, i)
                number_of_watched_episodes = season.get(
                    "number_of_watched_episodes")

                if number_of_watched_episodes == None:
                    number_of_watched_episodes = 0

                runtime += data.get("runtime") * number_of_watched_episodes
    else:
        raise InvalidParameter(
            "The watchStatus: {} is invalid -> valide arguments:{} ".format(
                type, ["Movie", "TV"]))

    return runtime