from datetime import datetime


def datatime_convert(unix_time):
    """Конвертирует время из формата UNIX в читаемый формат."""
    dt_object = datetime.fromtimestamp(int(unix_time))
    # Форматируем дату в формате ГГГГ-ММ-ДД_ЧЧ-ММ-СС
    formatted_date = dt_object.strftime(
        '%Y-%m-%d_at_%H-%M-%S').replace('-', '_')
    return formatted_date

# Пример использования
# Импорт в основной модуль (класс загрузчика)
# Вставить в заголовок файла импорт
# from modules.utils.time_convert import time_convert

# Пример использования
# time_convert(123456789)
