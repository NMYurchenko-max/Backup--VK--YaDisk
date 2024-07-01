import logging
import sys
from pathlib import Path

working_directory = Path.cwd()
log_file = working_directory.joinpath(r'modules/logs/app.log')


def setup_logging(
    log_file='app.log',
    log_level=logging.INFO,
    log_format='%(asctime)s %(levelname)s: %(message)s,'
):
    """Настройка логгера."""
    logger = logging.getLogger('my_logger')
    logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


logger = setup_logging()
logger.info('Пример использования внешним файлом')


def set_console_color(color_code):
    sys.stdout.write(color_code)


def reset_console_color():
    sys.stdout.write("\033[0m")
