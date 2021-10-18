import requests


class YaDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def upload_file(self, file_url, name_dir, file_name):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        path = f'{name_dir}/{file_name}.jpg'
        params = {'url': file_url, 'path': path}
        headers = self.get_headers()
        response = requests.post(url=upload_url, headers=headers, params=params)
        if response.status_code != 202:
            print(response.status_code)

    def create_dir(self, name_dir):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': name_dir}
        headers = self.get_headers()
        response = requests.put(url=url, headers=headers, params=params)
        if response.status_code == 201:
            print(f'Папка "{name_dir}" создана на Я.Диске')
        elif response.status_code == 409:
            print(f'Папка "{name_dir}" уже существует')
        else:
            print(response.status_code)