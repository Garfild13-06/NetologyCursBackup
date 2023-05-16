import VK
import YandexDisk
import params

from pprint import pprint
import requests
import os
import logging
import time


def exec_backup():
    log_file = f"{params.parrent_dir}/log.log"

    root_logger = logging.getLogger()
    root_logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(log_file, "a", "utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    root_logger.addHandler(handler)

    logging.info("---Start execute---")
    start = time.time()

    vk_api = VK.VK_api()
    ya_api = YandexDisk.YA_api()
    album_urls_list = []
    album_title = "Screenshots_space"
    user_id = 466978455
    logging.info(f"Запрашиваю фото из альбома пользователя VK")
    data = vk_api.photos_get(album_title=album_title, user_id=user_id).json()["response"]["items"]

    for photo in data:
        for size in photo["sizes"]:
            # самый большой размер фото идёт с типом `w`. Берём url'ы из словарей с указанным типом
            if size["type"] == "w":
                logging.info(
                    f"Получаю URL фотографии для скачивания и кол-во лайков и добавляю в список \n{size['url']}, {photo['likes']['user_likes']}")
                album_urls_list.append((size["url"], photo["likes"]["user_likes"]))

    for index, url in enumerate(album_urls_list):
        logging.info(f"Скачиваю все фото из альбома в локальную папку")
        with open(f"{os.getcwd()}\\photos\\{index + 1}_{url[1]}.jpg", "wb") as f:
            r = requests.get(url[0])
            f.write(r.content)
            logging.info(f"{os.getcwd()}\\photos\\{index + 1}_{url[1]}.jpg загружено")

    for root, dirs, files in os.walk(os.getcwd() + "\photos"):
        logging.info(f"Загрузка файлов на Яндекс Диск")
        for filename in files:
            logging.info(f"Загружаю{root}\{filename}")
            ya_api.disk_resources_upload(loadfile=f"{root}\{filename}", savefile=f"NetologyCursBackup/{filename}",
                                         replace=True)

    end = time.time()
    logging.info(f"Время выполнения: {end - start} секунд")
    logging.info("---End execute---")


exec_backup()
