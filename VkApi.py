import requests
from datetime import datetime


class VkApi:
    URL = 'https://api.vk.com/method/'
    photo_likes = {}
    def __init__(self, token):
        self.token = token

    def _get_user_id(self, user_name):
        '''
        :param user_name: id or short name
        :return: id
        '''
        url_user = self.URL + 'users.get'
        params = {
            "user_ids": user_name,
            "access_token": self.token,
            "v": "5.131"
        }
        res_json = requests.get(url=url_user, params=params).json()
        if 'error' in res_json:
            self.print_error_msg(res_json)
        else:
            return res_json['response'][0]['id']

    def get_albums(self, user_name):
        url_photos = self.URL + 'photos.getAlbums'
        user_id = self._get_user_id(user_name)
        if user_id:
            params = {
                "owner_id": user_id,
                "access_token": self.token,
                "v": "5.131"
            }
            res_json = requests.get(url=url_photos, params=params).json()
            print(res_json)
            if 'error' in res_json:
                self.print_error_msg(res_json)
            else:
                return res_json['response']['items']

    def get_album_photos(self, user_name, album):
        '''
        :param user_name: id or short name
        :return: [{inf_foto1}, {inf_foto2}, ...]
        '''
        url_photos = self.URL + 'photos.get'
        user_id = self._get_user_id(user_name)
        if user_id:
            params = {
                "owner_id": user_id,
                "access_token": self.token,
                "album_id": album,
                "extended": 1,
                "v": "5.131"
            }
            res_json = requests.get(url=url_photos, params=params).json()
            if 'error' in res_json:
                self.print_error_msg(res_json)
            else:
                return res_json['response']['items']

    def _unix_date_to_date(self, unix_date):
        date = str(datetime.fromtimestamp(unix_date).date())
        return '_'.join(date.split('-'))

    def get_max_size_and_url(self, photo):
        likes = str(photo['likes']['count'])

        if likes in VkApi.photo_likes:
            unix_date = photo['date']
            if VkApi.photo_likes[likes] == 1:
                name = f'{likes}_{self._unix_date_to_date(unix_date)}'
            else:
                name = f'{likes}_{self._unix_date_to_date(unix_date)}_{VkApi.photo_likes[likes]}'
            VkApi.photo_likes[likes] = VkApi.photo_likes.get(likes) + 1
        else:
            VkApi.photo_likes[likes] = 1
            name = likes

        size = photo['sizes'][-1]['type']
        photo_dict = {'file_name': f'{name}.jpg', 'size': size}
        url_photo = photo['sizes'][-1]['url']
        return photo_dict, url_photo

    def print_error_msg(self, response_json):
        print(f"Что-то пошло не так.\n"
              f"Код ошибки: {response_json['error']['error_code']}\n"
              f"Причина: {response_json['error']['error_msg']}")


class VkUser(VkApi):
