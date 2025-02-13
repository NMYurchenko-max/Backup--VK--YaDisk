import requests
import logging
import configparser
from tqdm import tqdmn
from urllib.parse import urlencode

from modules.utils.config_rw import read_or_update_config
from modules.utils.logger_setup import setup_logging
from modules.utils.tqdm_utils import my_progress_bar
from modules.utils.datatime_convert import datatime_convert

from modules.classes.vk_api_handler_media import VKApiHandlerMedia
from modules.classes.vk_api_handler_txt import VKApiHandlerText
from modules.classes.yadisk_handler import YaDiskApiHandler


class ContentScanner:
    def __init__(self, force_update=False):
        """_summary_

        Args:
            vkh_txt (_type_): _description_
            vkh_media (_type_): _description_
            yadisk_handler (_type_): _description_
        """
        self.vkh_txt = VKApiHandlerText(force_update)
        self.vkh_media = VKApiHandlerMedia(force_update)
        self.yadisk_handler = YaDiskApiHandler(force_update)
        self.response = self.response

    def get_common_params(self):
        return self.params

    def send_request(self, method, request_type='GET', **kwargs):
        common_params = self.get_common_params()
        params = {**common_params, **kwargs}
        url = f'{self.base_url}{method}'
        if request_type == 'GET':
            full_url = f'{url}?{urlencode(params)}'
            response = requests.get(full_url)
        elif request_type == 'PUT':
            response = requests.put(url, data=params, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            with tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                bar_format=(
                    '{l_bar}{bar}| {n_fmt}/{total_fmt}['
                    '{elapsed}<{remaining}, {rate_fmt}]')
            ) as progress_bar:
                for data in response.iter_content(chunk_size=1024):
                    progress_bar.update(len(data))
                    if progress_bar.total > 0:
                        progress_bar.set_description(
                            f"\033[92m{progress_bar}\033[0m")
        self.response = response.json()
        return self.response

    def scan_and_process_content(self):
        """
        Основной метод для сканирования и обработки контента.
        Этот метод может вызывать другие методы
        для выполнения конкретных задач,
        таких как загрузка медиафайлов на VK или Яндекс.Диск.
        """
        return self.send_request('users.get', user_ids=self.user_id)
        """
        Метод для получения информации о пользователе.
        :return: Информация о пользователе.
        """ 

    def upload_vk_media(self, media_path):
        """
        Загружает медиафайлы на VK через VKApiHandlerMedia.
        """
        # Здесь должна быть логика загрузки медиафайлов
        pass

    def process_vk_text(self):
        """
        Обрабатывает текстовые данные от VK через VKApiHandlerText.
        """
        # Здесь может быть логика обработки текстовых данных
        pass

    def upload_to_yandex_disk(self, file_path):
        """
        Загружает файлы на Яндекс.Диск через YaDiskApiHandler.
        """
        # Логика загрузки файла на Яндекс.Диск
        pass

    def upload_photo_to_yandex_disk(self, photo_url):
        # Реализация метода...
        pass

    def get_last_uploaded_photos(self):
        # Реализация метода...
        pass


if __name__ == '__main__':
    # Чтение конфигурации
    config_data = read_or_update_config(force_update=True)

    # Инициализация обработчиков
    vkh_txt = VKApiHandlerText(config_data)
    vkh_media = VKApiHandlerMedia(config_data)
    yadisk_handler = YaDiskApiHandler(config_data)
   
    # Создание экземпляра ContentScanner с обработчиками
    content_scanner = ContentScanner(vkh_txt, vkh_media, yadisk_handler)

    # Пример использования
    content_scanner.upload_vk_media('path/to/media')
    content_scanner.process_vk_text()
    content_scanner.upload_to_yandex_disk('path/to/file')

"""
# Другие методы...
    def downtloand_pfoto(self):
        print("Введите URL фотографии для загрузки (или 'exit' для выхода):")
        while True:
            user_input = input("Вы: ").strip()
            if user_input.lower() == 'exit':
                break
            try:
                photo_url = user_input
                disk_path = upload_photo_to_yandex_disk(photo_url)  
                # Используем метод класса ContentScanner
                print(f"Фото '{photo_url}' успешно загружено на Яндекс.Диск\
                     по пути: {disk_path}")
            except Exception as e:
                logger.error(f"Ошибка при загрузке фото: {e}")

    def print_last_uploaded_photos(self):
        # Выводит список последних загруженных фотографий
        last_photos = get_last_uploaded_photos()
        # Предполагается, что у вас есть такой метод
        if last_photos:
            for photo in last_photos:
                print(photo)
        else:
            print("Фотографий нет.")
"""
                                                           