from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse, parse_qs
import requests


# Ваши данные для OAuth2
client_id = '51904490'
client_secret = 'eLyHuApNp0V66Vpch3Vn'
redirect_uri = 'https://oauth.vk.com/nmyurchenko.http'
scope = [
    'phone', 'friends', 'wall', 'groups', 'messages', 'notifications',
    'stats', 'notes', 'photos', 'videos', 'docs', 'market', 'ads',
    'status', 'pages', 'offline', 'email'
]

# Базовые URL для OAuth2
authorization_base_url = 'https://oauth.vk.com/authorize'
token_url = 'https://oauth.vk.com/access_token'

# Создаем сессию OAuth2
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

# Генерируем URL для авторизации
authorization_url, state = oauth.authorization_url(authorization_base_url)
print(('Пожалуйста, перейдите по следующему URL и авторизуйте приложение:\n'
      + authorization_url))

# Пользователь перенаправляется и вводит URL перенаправления
redirected_url = input("Введите URL перенаправления: ")

# Извлекаем код авторизации из URL
parsed_url = urlparse(redirected_url)
query_params = parse_qs(parsed_url.fragment)
authorization_code = query_params['code'][0]
state = query_params['state'][0]
print("Строка соответствия states: ")
# Проверяем наличие кода авторизации
if authorization_code:
    print(f"Код авторизации: {authorization_code}")
else:
    print("Код авторизации не найден.")


# Функция для получения токена
def fetch_and_use_token(
    oauth,
    client_id,
    client_secret,
    redirect_uri,
    code=None,
    state=None
):
    try:
        token = oauth.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=redirected_url,
            state=state
        )
        print(f"Токен доступа: {token}")
        return token
    except Exception as e:
        print(f"Ошибка при получении токена: {e}")
        raise


# Получаем токен
try:
    token = fetch_and_use_token(
        oauth,
        client_id,
        client_secret,
        redirect_uri,
        authorization_code,
        state
    )
except Exception as e:
    print(e)

# Используем токен для запроса к VK API
# Например, можно импортировать токен
# и использовать его в запросах к VK API
token = {'access_token': 'your_access_token'}
user_id = '775884604'
user_info_url = (
    "https://api.vk.com/method/users.get?"
    "fields=bdate,city&access_token=" + token['access_token']
)
response = requests.get(user_info_url)
print(f"Ответ от VK API: {response.json()}")
