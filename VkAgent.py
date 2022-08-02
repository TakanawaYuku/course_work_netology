import requests
import os
import json
import Token
import Ya
import Agent
import time
import random as rnd
from pprint import pprint


class VkAgent(Agent.Social):
    url = 'https://api.vk.com/method/'

    def __init__(self, token, owner_id):
        self.params = {'access_token': token,
                       'v': '5.131', 'owner_id': owner_id}

    def __albums_id(self):
        albums_id = []
        photos_getalbums_url = self.url + 'photos.getAlbums'
        photos_getalbums_params = {'need_system': '1'}
        response = requests.get(photos_getalbums_url, params={
                                **self.params, **photos_getalbums_params}).json()

        for item in response['response']['items']:
            albums_id.append({
                'title': self._path_normalizer(item['title']),
                'id': item['id']
            })

        return albums_id

    @staticmethod
    def __get_items(item: dict):
        area = 0
        for size in item['sizes']:
            if size['height'] and size['width'] and size['height'] > 0 and size['width'] > 0:
                if size['height'] * size['width'] > area:
                    area = size['height'] * size['width']
                    image_res = f"{size['height']} * {size['width']}"
                    photo_url = size['url']
            else:
                flag = False
                for i in 'wzyx':
                    for size1 in item['sizes']:
                        if size1['type'] == i:
                            image_res = "данных нет"
                            photo_url = size1['url']
                            flag = True
                            break
                    if flag:
                        break
                break
        return image_res, photo_url

    def photos_info(self):
        total_photos_info = {}
        photos_get_url = self.url + 'photos.get'
        for album_id in self.__albums_id():
            print(f"Получаем данные из альбома: {album_id['title']}")
            time.sleep(rnd.randint(1, 5))
            photos_info = []
            file_names_count = {}
            photos_get_params = {'album_id': album_id['id'], 'extended': 1}
            response = requests.get(photos_get_url, params={
                                    **self.params, **photos_get_params}).json()
            if 'response' in response:
                for item in response['response']['items']:
                    image_resolution = self.__get_items(item)[0]
                    photo_url = self.__get_items(item)[1]
                    likes = item['likes']['count']
                    file_name = str(likes)
                    file_names_count[file_name] = file_names_count.get(
                        file_name, 0) + 1
                    photos_info.append({
                        'file_name': file_name,
                        'date': item['date'],
                        'url': photo_url,
                        'size': image_resolution
                    })
                for photo in photos_info:
                    if file_names_count[photo['file_name']] > 1:
                        photo['file_name'] += f"_{photo['date']}.jpg"
                    else:
                        photo['file_name'] += ".jpg"
                    del photo['date']

                total_photos_info[album_id['title']] = photos_info

        return total_photos_info


if __name__ == '__main__':
    FILE_DIR1 = "Vladimir"
    PATH_DIR1 = os.path.join(os.getcwd(), FILE_DIR1)
    vladimir = VkAgent(Token.TOKEN_VK, "9958238")
    pprint(vladimir.photos_info())
    vladimir.files_downloader(FILE_DIR1)
    michel_load = Ya.YaUploader(Token.TOKEN_YA)
    michel_load.upload(PATH_DIR1)

    path_ok = os.path.join(os.getcwd(), 'Test')
    ok1 = Ya.YaUploader(Token.TOKEN_YA)
    ok1.upload_recursive(path_ok)
