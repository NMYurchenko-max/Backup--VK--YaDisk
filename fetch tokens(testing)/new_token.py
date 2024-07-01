from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse, parse_qs
import requests
import base64
import hashlib
import secrets


def generate_pkce():
    """
    Генерирует пару code_verifier и code_challenge
    для использования в PKCE (Proof Key for Code Exchange).

    Returns:
        tuple: Кортеж, содержащий code_verifier и code_challenge.
    """
    code_verifier = base64.urlsafe_b64encode(
        secrets.token_bytes(32)).decode().rstrip("=")
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(
        code_challenge).decode().rstrip("=")
    return code_verifier, code_challenge


def get_authorization_code(client_id, redirect_uri):
    """
    Запрашивает у пользователя переход по URL для авторизации
    и возвращает authorization_code.

    Args:
        client_id (str): Идентификатор приложения VK.
        redirect_uri (str): URI, на который VK будет перенаправлять
        пользователя после авторизации.

    Returns:
        tuple: Кортеж, содержащий authorization_code и code_verifier.
    """
    code_verifier, code_challenge = generate_pkce()
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    # Формирование URL для авторизации с использованием PKCE
    authorization_url, _ = oauth.authorization_url(
        'https://oauth.vk.com/authorize',
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=[
            'user', 'wall', 'photo', 'video', 'status', 'docs', 'fave',
            'friends', 'groups', 'likes', 'messages'],
        code_challenge=code_challenge,
        code_challenge_method='S256'
    )
    print(
        f'Перейдите по URL и авторизуйте приложение:\n{authorization_url[0]}')
    redirected_url = input('Введите URL перенаправления после авторизации: ')
    parsed_url = urlparse(redirected_url)
    query_params = parse_qs(parsed_url.fragment)
    # Извлечение authorization_code из URL перенаправления
    authorization_code = (
        query_params['code'][0]
        if 'code' in query_params and query_params['code']
        else None
    )
    if authorization_code:
        print(f"Код авторизации: {authorization_code}")
    else:
        print("Код авторизации не найден.")
        exit()
    return authorization_code, code_verifier


def exchange_code_for_token(
    client_id,
    client_secret,
    redirect_uri,
    authorization_code,
    code_verifier
):
    """
    Обменивает authorization_code на токен доступа.

    Args:
        client_id (str): Идентификатор приложения VK.
        client_secret (str): Секретный ключ приложения VK.
        redirect_uri (str): URI для перенаправления после авторизации.
        authorization_code (str): Код авторизации, полученный от VK.
        code_verifier (str): Верификатор, используемый для PKCE.

    Returns:
        str: Токен доступа или None, если произошла ошибка.
    """
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
        'code_verifier': code_verifier
    }
    response = requests.post('https://oauth.vk.com/access_token', data=data)
    if response.ok:
        json_response = response.json()
        if 'access_token' in json_response:
            return json_response['access_token']
        else:
            print(
                f'Ошибка при получении токена: '
                f'{json_response.get("error_description", "Unknown error")}'
            )
            return None
    else:
        print(f'Ошибка запроса токена: {response.text}')
        return None


def main():
    """
    Основная логика скрипта: получение authorization_code
     и обмен его на токен доступа.
    """
    client_id = '51904490'
    client_secret = 'eLyHuApNp0V66Vpch3Vn'
    redirect_uri = 'https://oauth.vk.com/nmyurchenko.http'
    # Получение кода авторизации
    authorization_code, code_verifier = (
        get_authorization_code(client_id, redirect_uri)
    )
    # Обмен кода авторизации на токен доступа
    access_token = (
        exchange_code_for_token(
            client_id,
            client_secret,
            redirect_uri,
            authorization_code,
            code_verifier
        )
    )
    if access_token:
        print(f'Токен доступа: {access_token}')
    else:
        print('Не удалось получить токен доступа.')
    exit()


if __name__ == '__main__':
    main()

    """
В этом примере additional_args — это словарь,
который может содержать любые другие параметры, кроме redirect_uri.
Мы явно передаем redirect_uri как аргумент функции authorization_url(),
а затем используем **additional_args для передачи всех остальных параметров,
которые мы хотим добавить. Таким образом, redirect_uri указывается только один
 раз, избегая ошибку дублирования.

Если вы не используете дополнительные параметры и ваш вызов функции выглядит
именно так, как я показал выше, то проблема может быть где-то еще. В таком
случае, стоит проверить, правильно ли вы используете библиотеку и не передаете
ли где-то еще redirect_uri в другом месте кода. Также полезно проверить
документацию  к используемой версии requests_oauthlib,
чтобы убедиться, что все делается согласно рекомендациям.

Если ошибка сохраняется, возможно, проблема кроется в самой библиотеке
 или в том, как она используется. В таком случае, рекомендуется проверить
актуальную документацию или исходный код библиотеки для выявления
причины ошибки. Также может помочь обновление до последней версии библиотеки
или поиск решений, связанных с этой конкретной ошибкой в интернете.

Чтобы запросить список версий библиотеки в терминале, вы можете использовать
команду `pip list` для получения списка всех установленных библиотек
и их версий. Если вы хотите узнать версию конкретной библиотеки,
например `requests_oauthlib`, вы можете использовать команду `pip show`.
Вот как это сделать:

1. Откройте терминал на вашем компьютере.
2. Введите следующую команду для просмотра всех установленных
библиотек и их версий:
   ```
   pip list
   ```
   Эта команда покажет вам список всех установленных библиотек
    в вашем текущем окружении Python, включая их версии.

3. Если вы хотите узнать версию конкретной библиотеки, например
 `requests_oauthlib`, используйте команду `pip show`:
   ```
   pip show requests_oauthlib
   ```
   Эта команда выведет информацию о библиотеке `requests_oauthlib`,
    включая ее версию.

Если вы хотите обновить библиотеку до последней версии, используйте команду
 `pip install --upgrade` с именем библиотеки. Например,
 чтобы обновить `requests_oauthlib`, выполните:
   ```
   pip install --upgrade requests_oauthlib
   ```

Эти команды помогут вам управлять версиями библиотек в вашем проекте
 и убедиться, что вы используете последние версии,
 которые могут содержать исправления ошибок и улучшения.
    """
