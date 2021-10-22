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

def upload_photos(album_name, all_photos):
    new_dir_yadisk = f'album_{album_name}'
    ya_user.create_dir(new_dir_yadisk)
    for photo in tqdm(all_photos):
        photo_name = photo['file_name']
        photo_url = photo.pop('url')
        ya_user.upload_file(file_url=photo_url, name_dir=new_dir_yadisk, file_name=photo_name)
    return all_photos


if __name__ == '__main__':
    limit_photos = 5
    user_name = "begemot_korovin"
    # user_name = 'mariacoruja'
    album = "profile"
    vk_user = VkApi(TOKEN_VK, user_name)
    ya_user = YaDisk(TOKEN_YADISK)

    all_albums = vk_user.get_all_albums()
    if all_albums:
        print(all_albums)
    # album = 228512720
    all_album_photos = vk_user.get_all_photos(album, limit_photos)
    for_json = upload_photos(album, all_album_photos)
    write_to_json(album, for_json)