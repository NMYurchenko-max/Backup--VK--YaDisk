import requests
from urllib.parse import urlencode
from modules.utils.config_rw import read_or_update_config


class VKApiHandlerMedia:
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
            'v': self.version}

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
  
    def upload_media(self, media_path):
        """
        Загружает медиафайлы на VK.
        """
        # Запрос к VK API для получения URL для загрузки
        # Загрузка видео
        video_path = 'path_to_your_video.mp4'
        video = upload.video(video_path, name='Video Title', description='Video Description')
        video_url = f"video{video['owner_id']}_{video['video_id']}"
        print(f"Ссылка на загруженное видео: {video_url}")  

        # Загрузка фото
        photo_path = 'path_to_your_photo.jpg'
        photo = upload.photo(photo_path)
        photo_url = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
        print(f"Ссылка на загруженное фото: {photo_url}")
    
    def entry_point(self):
        """
        Основная точка входа для демонстрации работы
        с VK API через данный класс.
        """
        print(self.user_info())
        self.get_wall_photos()


if __name__ == '__main__':
    config_reader = read_or_update_config()
    config_data = config_reader.read_or_update_config()
    vk_config = config_data.get('VK', {})

    vkh_media = VKApiHandlerMedia(vk_config)
    vkh_media.entry_point()


"""

# Авторизация в VK
vk_session = vk_api.VkApi('your_login', 'your_password')
vk_session.auth()

# Загрузка фото
upload = vk_api.VkUpload(vk_session)
photo_path = 'path_to_your_photo.jpg'
photo = upload.photo(photo_path)
photo_url = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
print(f"Ссылка на загруженное фото: {photo_url}")

"""