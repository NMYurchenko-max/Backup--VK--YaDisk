import configparser


def read_or_update_config(force_update=False, album_id=None):
    """
    Считывает или обновляет конфигурационный файл и возвращает данные для VK,
    Яндекс.Диска. Можно добавить любое количество секций данных,
    например 'Photo'...
    Если информация отсутствует, предлагает пользователю её ввести.
    Аргумент force_update определяет, следует ли запрашивать ввод данных
    для отсутствующих полей.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    config_data = {}

    # Определяем секции для чтения и обновления
    sections = ['VK', 'YaDisk']

    for section in sections:
        if not config.has_section(section):
            config.add_section(section)

        tokens = {}
        keys = {
            'VK': ['user_id', 'access_token'],
            'YaDisk': ['token_ya', 'folder_path'],
            }.get(section, [])  # Получаем ключи для текущего раздела

        for key in keys:
            try:
                value = config.get(section, key, fallback=None)
            except configparser.NoOptionError:
                if force_update:
                    # Запрашиваем у пользователя ввод данных,
                    # если значение отсутствует и force_update=True
                    value = input(f"Введите {key} для {section}: ")
                else:
                    raise ValueError(
                        f"Необходимо предоставить\
                             значение для {key} в секции {section}")

            tokens[key] = value

        config_data[section] = tokens

    # Автоматическое сохранение изменений в config.ini
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    return config_data


"""
# Пример создания экземплярор классов VKApiHandlerMedia, VKApiHandlerText,
#  YaDiskApiHandler и на основе данных секции

config_data = read_or_update_config()
config_data['VK'] = {}

vk_config = config_data.get('VK', {})
vkh_media = VKApiHandlerMedia(vk_config)
vkh_media.entry_point()

vk_config = config_data.get('VK', {})
vkh_txt = VKApiHandlerText(vk_config)
vkh_txt.entry_point()

config_data['YaDisk'] = {}
yadisk_config = config_data.get('YaDisk', {})
yadisk_handler = YaDiskApiHandler(yadisk_config)


# Пример использования
from modules.config_rw import read_or_update_config

if __name__ == '__main__':
      # Чтение или обновление конфигурации для всех сервисов
    config_data = read_or_update_config(
    sections={
        'VK': ['access_token', 'user_id', 'version'],
        'YaDisk': ['token_ya', 'folder_path'],
        }, force_update=True)

    # Создание экземпляров классов с указанием конфигурации
    vk_config = config_data.get('VK', {})
    vkh_txt = VKApiHandlerText(vk_configforce_update=True)
    
    vk_config = config_data.get('VK', {})
    vkh_txt = VKApiHandlerText(vk_config)
    vkh_media = VKApiHandlerMedia(vk_config)

    yadisk_config = config_data.get('YaDisk', {})
    yadisk_handler = YaDiskApiHandler(yadisk_config)

    # Создание экземпляра ContentScanner с обработчиками
    content_scanner = ContentScanner(vkh_txt, vkh_media, yadisk_handler)
    """
