import requests
from consumatio.gateways.movie_details_to_dict import * 
from consumatio.gateways.movie_providers_to_dict import * 
from consumatio.gateways.movie_images_to_dict import *
from consumatio.gateways.tv_details_to_dict import *
from consumatio.gateways.tv_providers_to_dict import *
from consumatio.gateways.tv_images_to_dict import *
from consumatio.gateways.season_details_to_dict import *
from consumatio.gateways.season_images_to_dict import * 
from consumatio.gateways.episode_details_to_dict import * 
from consumatio.gateways.episode_images_to_dict import *
from consumatio.external.db import cache
from consumatio.external.db import is_cached
from consumatio.external.db import get_from_cache

class Tmdb():
    
    def get_movie_details(self, movie_id):
        query = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c4bd02adee6e73c4d17e69b039267c90&language=en-US'
        if (is_cached(query)):
           data = get_from_cache(query) 
        else:
           data = requests.get(query).json() 
           cache(query, str(data))
        return movie_details_to_dict(data)

    def get_movie_providers(self, movie_id, country):
        query = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key=c4bd02adee6e73c4d17e69b039267c90'
        if (is_cached(query)):
           data = get_from_cache(query) 
        else:
           data = requests.get(query).json() 
           cache(query, str(data))
        data = data['results'][country]
        return movie_providers_to_dict(data)

    def get_movie_images(self, movie_id):
        query = f'https://api.themoviedb.org/3/movie/{movie_id}/images?api_key=c4bd02adee6e73c4d17e69b039267c90'
        if (is_cached(query)):
           data = get_from_cache(query) 
        else:
           data = requests.get(query).json() 
           cache(query, str(data))
        return movie_images_to_dict(data)

    def get_tv_details(self, tv_id):
        query = f'https://api.themoviedb.org/3/tv/{tv_id}?api_key=c4bd02adee6e73c4d17e69b039267c90&language=en-US'
        if (is_cached(query)):
           data = get_from_cache(query) 
        else:
           data = requests.get(query).json() 
           cache(query, str(data)) 
        return tv_details_to_dict(data)

    def get_tv_providers(self, tv_id, country):
        query = f'https://api.themoviedb.org/3/tv/{tv_id}/watch/providers?api_key=c4bd02adee6e73c4d17e69b039267c90' 
        if (is_cached(query)):
           data = get_from_cache(query) 
        else:
           data = requests.get(query).json() 
           cache(query, str(data)) 
        data = data['results'][country]
        return tv_providers_to_dict(data)

    def get_tv_images(self, tv_id):    
        query = f'https://api.themoviedb.org/3/tv/{tv_id}/images?api_key=c4bd02adee6e73c4d17e69b039267c90'
        if (is_cached(query)):
           data = get_from_cache(query) 
        else:
           data = requests.get(query).json() 
           cache(query, str(data)) 
        return tv_images_to_dict(data)

    def get_season_details(self, tv_id, season_number):
        query = f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}?api_key=c4bd02adee6e73c4d17e69b039267c90'
        if (is_cached(query)):
           data = get_from_cache(query) 
        else:
           data = requests.get(query).json() 
           cache(query, str(data)) 
        return season_details_to_dict(data, tv_id)

    def get_season_images(self, tv_id, season_number):
        query = f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}/images?api_key=c4bd02adee6e73c4d17e69b039267c90' 
        if (is_cached(query)):
           data = get_from_cache(query) 
        else:
           data = requests.get(query).json() 
           cache(query, str(data))
        return season_images_to_dict(data)

    def get_episode_details(self, tv_id, season_number, episode_number):
        query = f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}/episode/{episode_number}?api_key=c4bd02adee6e73c4d17e69b039267c90'
        if (is_cached(query)):
           data = get_from_cache(query) 
        else:
           data = requests.get(query).json() 
           cache(query, str(data)) 
        return episode_details_to_dict(data)

    def get_episode_images(self, tv_id, season_number, episode_number):
        query = f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}/episode/{episode_number}/images?api_key=c4bd02adee6e73c4d17e69b039267c90'
        if (is_cached(query)):
           data = get_from_cache(query) 
        else:
           data = requests.get(query).json() 
           cache(query, str(data))
        return episode_images_to_dict(data)
        