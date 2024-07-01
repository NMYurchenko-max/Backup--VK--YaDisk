import requests
from urllib.parse import urlencode

from modules.utils.config_rw import read_or_update_config


class VKApiHandlerText:
    API_BAS_URL = 'https://api.vk.com/method'

    """
    Класс для работы с API VK.
    Аргументы:
    - access_token (str): Токен доступа VK.
    - user_id (str): ID пользователя VK.
    - version (str): Версия API VK.
    """
    def __init__(self, force_update=False):
        config_data = read_or_update_config(force_update)
        self.vk_config = config_data.get('VK', {})
        self.access_token = self.vk_config.get('access_token')
        self.user_id = self.vk_config.get('user_id')
        self.params = {
            'access_token': self.access_token,
            'user_id': self.user_id,
            'v': '5.199'
        }

    def get_common_params(self):
        return {
            'access_token': self.access_token,
            'v': self.version
        }

    def send_request(self, method, **kwargs):
        common_params = self.get_common_params
        params = {**self.params, **common_params, **kwargs}
        url = f'{self.API_BAS_URL}{method}'
        encoded_params = urlencode(params)
        full_url = f'{url}?{encoded_params}'
        response = requests.get(full_url)
        return response.json()

    def user_info(self):
        """
        Метод для получения информации о пользователе.
        :return: Информация о пользователе.
        """
        return self.send_request('users.get', user_ids=self.id)

    def get_status(self):
        """
        Метод для получения статуса пользователя.
        :return: Статус пользователя.
        """
        response = requests.get(self.send_request('status.get'))
        return response.json().get('response', {})

    def set_status(self, new_status):
        """
        Метод для установки статуса пользователя.
        :param new_status: Текст статуса пользователя.
        :return: Статус пользователя.
        """
        params = {'text': new_status}
        response = requests.get(self.send_request('status.set', params=params))
        return response.json().get('response', {})

    def replace_status(self, target, replace_status):
        """
        Метод для замены статуса пользователя.
        :param target: ID пользователя, которому нужно заменить статус.
        :param replace_status: Текст статуса пользователя.
            :return: Статус пользователя.
        """
        status = self.get_status().get('response', {}).get('text', '')
        new_status = status.replace(target, replace_status)
        self.set_status(new_status)

    def get_friends(self):
        """
        Метод для получения списка друзей пользователя.
        :return: Список друзей пользователя.
        """
        response = requests.get(self.send_request('friends.get'))
        return response

    def get_messages(self, count=10):
        """
        Получает сообщения от друзей.
        Args:
            count: Количество сообщений,(int, optional)
        Return: list: Список сообщений от друзей.
        """
        response = requests.get(self.send_request('messages.get', count=count))
        return response.json()['respons']['item']

    def get_wall_photos(self):
        """
        Получает ссылки на фотографии со стены ВК.
        Return: list: Список ссылок на фотографии со стены ВК.
        """
        params = {'owner_id': self.user_id, 'count': 5, 'extended': 1}
        response = requests.get(self.send_request(
            'photos.getWall', params=params))
        photos = response.json().get('response', {}).get('items', [])
        photo_urls = [photo['sizes'][-1]['url'] for photo in photos]
        return photo_urls

    def entry_point(self):
        """
    Основная точка входа для демонстрации работы
    с VK API через данный класс.

    Эта функция выполняет следующие действия:
    1. Выводит информацию о текущем пользователе VK.
    2. Получает и выводит текущий статус пользователя.
    3. Запрашивает у пользователя ввод нового текстового статуса.
    4. Устанавливает новый статус пользователя на основе введенного текста.
    5. Заменяет часть текущего статуса на введенный текст
    (в данном случае, вся строка заменяется).
    6. Выводит список друзей текущего пользователя.
  
    Для выполнения этих действий используются различные
    методы класса VKApiHandlerText, включая отправку запросов
     к VK API для получения и изменения данных пользователя.
        """
        print(self.user_info())
        self.get_status()
        new_status = input("Введите текст статуса: ")
        self.set_status(new_status)
        self.replace_status(new_status, new_status)
        print()
        self.get_friends()


if __name__ == '__main__':
    config_reader = read_or_update_config()
    config_data = config_reader.read_or_update_config()
    vk_config = config_data.get('VK', {})

    vkh_txt = VKApiHandlerText(vk_config)
    vkh_txt.entry_point()
