import requests
from time import sleep
import logging


class YA_api:

    def __init__(self):
        self.access_token = ""
        self.url = "https://cloud-api.yandex.net/v1"
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                        'Authorization': f'OAuth {self.access_token}'}

    def disk_resources_upload(self, loadfile, savefile, replace=False):
        """Загрузка файла.
        savefile: Путь к файлу на Диске
        loadfile: Путь к загружаемому файлу
        replace: true or false Замена файла на Диске"""
        method = "/disk/resources/upload"
        URL = self.url + method
        res = requests.get(f'{URL}?path={savefile}&overwrite={replace}', headers=self.headers).json()
        with open(loadfile, 'rb') as f:
            try:
                requests.put(res['href'], files={'file': f})
                logging.info(f"Файл {loadfile} загружен в {savefile}")
            except KeyError:
                logging.error(res)
