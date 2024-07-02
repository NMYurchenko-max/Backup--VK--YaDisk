from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse, parse_qs
import requests

# Мои данные для OAuth2 (scorp должны совпадать с приложением)
client_id = ''
client_secret = ''
redirect_uri = 'https://oauth.vk.com/nmyurchenko.http'
scope = scope = [
    'phone', 'friends', 'wall', 'groups', 'messages', 'notifications',
    'stats', 'notes', 'photos', 'videos', 'docs', 'market', 'ads',
    'status', 'pages', 'offline', 'email'
]
# Базовые url для для OAuth2
authorization_base_url = 'https://oauth.vk.com/authorize'
token_url = 'https://oauth.vk.com/access_token'
# Создаем сессию OAuth2
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
# Генерируем URL для авторизации
authorization_url, state = oauth.authorization_url(authorization_base_url)
print(('Пожалуйста, перейдите по следующему URL и авторизуйте приложение:\n'
      + authorization_url))
# Пользователь перенаправляет и вводит URL перенаправления
redirected_url = input("Введите URL перенаправления: ")
# Извлекаем код авторизации из URL
parsed_url = urlparse(redirected_url)
query_params = parse_qs(parsed_url.fragment)
authorization_code = query_params['code'][0]
authorization_state = query_params['code'][0]
# Проверяем наличие кода авторизации
if authorization_code:
    print(f"Код авторизации: {authorization_code}")
else:
    print("Код авторизации не найден.")


# Определение функции fetch_and_use_token
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
            authorization_response=redirected_url
        )
        print(f"Токен доступа: {token}")
        return token
    except Exception as e:
        print(f"Ошибка при получении токена: {e}")
        authorization_code = input("Введите полученный код авторизации: ")
        state = input("Введите переданный state: ")
        token = get_access_token(
            client_id,
            client_secret,
            redirect_uri,
            authorization_code,
            state
        )
        print(f"Токен доступа: {token}")
        return token


# Определение функции get_access_token
def get_access_token(client_id, client_secret,
                     redirect_uri, code, code_verifier=''):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code,
        'grant_type': authorization_code,
        'code_verifier': code_verifier,
        'state': state
    }
    response = requests.post('https://oauth.vk.com/access_token', data=data)
    if response.ok:
        json_response = response.json()
        if 'access_token' in json_response:
            return json_response['access_token']
        else:
            print("Ошибка при получении токена:",
                  json_response.get('error_description', 'Unknown error'))
            return None
    else:
        print("Ошибка при запросе токена:", response.text)
        return None


# импортируем access_token
token = {'access_token': 'your_access_token'}

# Пример запроса к VK API для получения информации о профиле пользователя
user_id = ''
user_info_url = (
    "https://api.vk.com/method/users.get?"
    "fields=bdate,city&access_token="
    "{token['access_token']}"
)
response = requests.get(user_info_url)
print(f"Ответ от VK API: {response.json()}")
