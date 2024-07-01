import requests
from urllib.parse import urlencode
from tqdm import tqdm
from modules.utils.config_rw import read_or_update_config


class YaDiskApiHandler:
    base_url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, force_update=False):
        config_data = read_or_update_config(force_update)
        self.yadisk_config = config_data.get('YaDisk', {})
        self.token_ya = self.yadisk_config.get('token_ya')
        self.folder_path = self.yadisk_config.get('folder_path')
        self.params = {
            'path': self.folder_path,
            'access_token': self.token_ya
        }
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

    def download_file(self, file_path):
        """
        Загружает файл на Яндекс.Диск.
        """
        method = '/download'
        params = {'path': file_path}
        response = self.send_request(method, request_type='GET', **params)
        # Обработайте ответ по своему усмотрению
        #  сохранить файл локально:
        if response.status_code == 200:
            file_name = file_path.split('/')[-1]
            file_path = f'downloads/{file_name}'
            print(file_path)
            with open(file_path, 'wb') as file:
                file.write(response.content)
                print(f'Файл {file_name} успешно загружен на Яндекс.Диск')
        else:
            print('Не удалось загрузить файл на Яндекс.Диск')
            print(response)
            # Возвращаем информацию о загруженном файле
            file_info = response.json()
            file_url = file_info['href']
            print(f"Ссылка на загруженный файл: {file_url}")
            return file_info

    def delete_file(self, file_path):
        """
        Удаляет файл с Яндекс.Диска.
        """
        method = '/trash'
        params = {'path': file_path}
        response = self.send_request(method, request_type='PUT', **params)
        # Обработайте ответ по своему усмотрению
        # Например, вы можете добавить свою логику обработки ответа
        # Например, вы можете проверить успешность удаления:
        if response.get('success', False):
            print(f'Файл {file_path} успешно удален с Яндекс.Диска')
        else:
            print('Не удалось удалить файл с Яндекс.Диска')
            print(response)
   
    def entry_point(self):
        """
        Основная точка входа для демонстрации работы
        с Яндекс.Диском через данный класс.
        """


if __name__ == '__main__':
    # Чтение или обновление конфигурации для всех сервисов
    config_data = read_or_update_config(force_update=True)  
    # Вы можете установить force_update=True, если нужно обновить конфигурацию

    # Инициализация обработчика Яндекс.Диска
    yadisk_config = config_data.get('YaDisk', {})
    yadisk_handler = YaDiskApiHandler(yadisk_config)

    # Загрузка файла на Яндекс.Диск
    yadisk_handler.download_file('path/to/file')