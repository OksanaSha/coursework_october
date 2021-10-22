import requests
from datetime import datetime


class VkApi:

    def __init__(self, token, user_name):
        self.token = token
        self.user_name = user_name
        self.id = self._get_user_id(user_name)

    URL = 'https://api.vk.com/method/'
    photo_likes = {}

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

    def get_all_albums(self):
        url_photos = self.URL + 'photos.getAlbums'
        if self.id:
            params = {
                "owner_id": self.id,
                "access_token": self.token,
                "v": "5.131"
            }
            res_json = requests.get(url=url_photos, params=params).json()
            if 'error' in res_json:
                self.print_error_msg(res_json)
            else:
                albums_id_and_name = {}
                count_albums = res_json['response']['count']
                print(f'Доступные альбомы "{self.user_name}" - {count_albums}')
                if count_albums != 0:
                    for album in res_json['response']['items']:
                        album_dict = {album['id']: album['title']}
                        albums_id_and_name.update(album_dict)
                    return albums_id_and_name


    def _get_album_photos_inf(self, album):
        '''
        :param user_name: id or short name
        :return: [{inf_foto1}, {inf_foto2}, ...]
        '''
        url_photos = self.URL + 'photos.get'
        if self.id and album:
            params = {
                "owner_id": self.id,
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

    def get_all_photos(self, album, limit):
        photos_name_and_size = []
        # all_urls = []
        photos_inf = self._get_album_photos_inf(album)
        if photos_inf:
            if limit > len(photos_inf):
                print(f"В альбоме {album} фотографий меньше {limit}, "
                      f"будет загружено {len(photos_inf)} шт.")
            for photo in photos_inf[:limit]:
                photo_inf_dict = self.get_max_size_and_url(photo)
                photos_name_and_size.append(photo_inf_dict)
                # all_urls.append(photo_url)
            return photos_name_and_size


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
        url_photo = photo['sizes'][-1]['url']
        photo_dict = {'file_name': f'{name}.jpg', 'size': size, 'url': url_photo}
        return photo_dict

    def print_error_msg(self, response_json):
        print(f"Что-то пошло не так.\n"
              f"Код ошибки: {response_json['error']['error_code']}\n"
              f"Причина: {response_json['error']['error_msg']}")

