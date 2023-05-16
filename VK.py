import requests
from time import sleep
import logging



class VK_api:
    def __init__(self):
        self.access_token = ""
        self.url = "https://api.vk.com/method/"
        self.vk_app_name = "netology_aim"
        self.vk_app_id = "51622064"
        self.v = "5.131"

    def photos_get(self, album_title, user_id=""):
        logging.info(f"Получаю информацию о фотографиях в альбоме {album_title}")
        # между выполнениями делаю паузу в 0.3 секунды, чтобы не попасть под ограничения по колву использования API
        sleep(0.3)
        method = "photos.get"
        # получаю данные об альбоме по его названию и ID пользователя
        r = self.photos_getAlbumIdByTitle(album_title, user_id)
        # получаю id альбома
        album_id = r["id"]
        # получаю кол-во элементов в альбоме
        count = r["size"]
        params = {
            "access_token": self.access_token,
            "v": self.v,
            "owner_id": user_id,
            "album_id": album_id,
            "count": count,
            "extended": 1,
        }
        url = self.url + method
        result = requests.get(url=url, params=params)
        return result

    def photos_getAlbumIdByTitle(self, title, user_id=""):
        logging.info(f"Ищу id альбома по заголовку: `{title}` и пользователю: `{user_id}`")
        method = "photos.getAlbums"
        params = {
            "access_token": self.access_token,
            "v": self.v,
            "owner_id": user_id,
        }
        url = self.url + method

        result = requests.get(url=url, params=params)
        for album in result.json()["response"]["items"]:
            if album["title"] == title:
                logging.info(f"Альбом найден")
                return album
