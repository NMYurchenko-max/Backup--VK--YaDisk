from modules.content_skanner import ContentScanner
from openai import OpenAI
import requests
from pathlib import Path
import logging


class Bot:
    def __init__(self):
        self.scanner = ContentScanner(
            ya_token="ваш_yandex_token",
            user_id="ваш_vk_id",
            access_token="ваш_access_token")
        # Инициализация клиента API OpenAI и ContentScanner
        self.client = OpenAI(
            api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I",
            base_url="https://api.proxyapi.ru/openai/v1",
        )
        # Список для хранения истории разговора
        self.conversation_history = []
        
        # Инициализация логгера
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        # Инициализация бота
        self.run()

    def run(self):
        print("Добро пожаловать Вы можете загрузить фотографии на Яндекс.Диск\
             или увидеть последние загруженные фотографии.")
        while True:
            user_input = input("Вы: ").strip()
            if user_input.lower() == 'exit':
                print("До свидания!")
                break
            # Здесь может быть логика обработки ввода пользователя
            #  и взаимодействия с ContentScanner
            # Основной цикл бота
            print("Добро пожаловать. Я ваш бот-помощник.")
            while True:
                print("\nВыберите действие:")
                print("1. Загрузить фотографию на Яндекс.Диск")
                print("2. Посмотреть последние фотографии")
                print("3. Помощь")
                print("4. Выход")
                print("5. Поговорить со мной")  # Новое действие

                action = input("Введите номер действия: ")
                if action == "1":
                    upload_photos()
                elif action == "2":
                    print_last_uploaded_photos()
                elif action == "3":
                    print("""Доступные действия:
                        \n1.Загрузить фотографию\n2. Посмотреть последние фото
                        \n3. Помощь\n4. Поговори со мной\5. Закрыть бот.""")
                elif action == "5":
                    print("До свидания!")
                    break
                elif action == "4":
                    print("Сейчас вы поговорите со мной. Что вас интересует?")
                    user_input = input("Вы: ").strip()
                    self.conversation_history.append(
                        {"role": "user", "content": user_input})

                    chat_completion = self.client.chat.completions.create(
                        model="gpt-3.5-turbo-1106",
                        messages=self.conversation_history
                    )

                    ai_response_content = chat_completion.choices[0].message.content
                    print("AI:", ai_response_content)
                    self.conversation_history.append({
                        "role": "system", "content": ai_response_content})
                    # Опционально: условие для выхода из цикла
                    # (например, если пользователь ввел 'exit')
                    if user_input.lower() == 'exit':
                        break

    def download_photos():
        """Загружает фотографии на Яндекс.Диск."""
        print("Введите URL фотографии для загрузки (или 'exit' для выхода):")
        while True:
            user_input = input("Вы: ").strip()
            if user_input.lower() == 'exit':
                break
            try:
                photo_url = user_input
                disk_path = scanner.upload_photo_to_yandex_disk(photo_url)  
                # Используем метод класса ContentScanner
                print(f"Фото '{photo_url}' успешно загружено на Яндекс.Диск\
                     по пути: {disk_path}")
            except Exception as e:
                logger.error(f"Ошибка при загрузке фото: {e}")

        def print_last_uploaded_photos():
            """Выводит список последних загруженных фотографий."""
            last_photos = scanner.get_last_uploaded_photos()
            # Предполагается, что у вас есть такой метод
            if last_photos:
                for photo in last_photos:
                    print(photo)
            else:
                print("Фотографий нет.")


"""
Объяснение кода
Импорт библиотек: Мы импортируем необходимые библиотеки для работы
 с API OpenAI, отправки HTTP-запросов и работы с файловой системой.
Настройка логирования: Создаем логгер для отслеживания ошибок и важных событий.
Инициализация клиента API OpenAI и ContentScanner: Здесь вы должны заменить
"ваш_api_ключ" на ваш реальный API-ключ OpenAI
Основной цикл бота: Бот предлагает пользователю выбрать действие из списка и
 выполняет соответствующую команду. Если пользователь выбирает "Помощь",
 бот выводит список доступных действий.
Функции для загрузки фотографий и просмотра последних загруженных фотографий:
Эти функции предполагают, что у вас уже есть реализация методов
в вашем классе ContentScanner.
Этот код представляет собой базовый шаблон для создания
интерактивного консольного бота, который может быть расширен
и адаптирован под ваши конкретные требования.
Таким образом, вы можете использовать класс ContentScanner для выполнения
различных задач, связанных с вашим приложением,
прямо из вашего консольного бота.
Это позволяет централизованно управлять всеми операциями,
связанными с вашим проектом,
и обеспечивает удобный интерфейс для взаимодействия с пользователем.
"""
