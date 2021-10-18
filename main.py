import json
from tqdm import tqdm
from VkApi import VkApi
from YaDisk import YaDisk


TOKEN_VK = ''
TOKEN_YADISK = ''


def write_to_json(album, photos_inf_list):
    data = {album: photos_inf_list}
    json_name = f'album_{album}.json'
    with open(json_name, 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':
    limit_photos = 15
    user_name = "begemot_korovin"
    album_vk = "profile"
    vk_user = VkApi(TOKEN_VK)
    ya_user = YaDisk(TOKEN_YADISK)

    album_photos_inf = vk_user.get_album_photos(user_name, album_vk)
    photos_name_and_size = []
    if limit_photos > len(album_photos_inf):
        print(f"Фотографий профиля меньше {limit_photos}, "
              f"будет загружено {len(album_photos_inf)} шт.")

    new_dir_yadisk = 'vk_profile'
    ya_user.create_dir(new_dir_yadisk)

    for photo in tqdm(album_photos_inf[:limit_photos]):
        photo_inf_dict, photo_url = vk_user.get_max_size_and_url(photo)
        photo_name = photo_inf_dict['file_name']
        ya_user.upload_file(file_url=photo_url, name_dir=new_dir_yadisk, file_name=photo_name)
        photos_name_and_size.append(photo_inf_dict)

    write_to_json(album_vk, photos_name_and_size)