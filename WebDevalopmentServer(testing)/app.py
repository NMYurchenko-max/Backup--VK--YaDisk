from flask import Flask, redirect, request, session, send_from_directory
# import requests
from requests_oauthlib import OAuth2Session


# Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'
# Замените на ваш секретный ключ для сессий Flask

# Константы для OAuth2 сессии
client_id = '51904490'
client_secret = 'eLyHuApNp0V66Vpch3Vn'
redirect_uri = 'https://oauth.vk.com/nmyurchenko.http'
# Убедитесь, что это ваш Redirect URI
scope = [
    'phone', 'friends', 'wall', 'groups', 'messages', 'notifications',
    'stats', 'notes', 'photos', 'videos', 'docs', 'market', 'ads',
    'status', 'pages', 'offline', 'email'
]


@app.route('/login')
def login():
    """
    Маршрут для начала процесса авторизации через VK.
    Создает OAuth2 сессию и перенаправляет пользователя
     на страницу авторизации VK.
    """
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url(
        'https://oauth.vk.com/authorize')
    session['oauth_state'] = state
    # Сохраняем состояние в сессии для последующей проверки
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    """
    Обрабатывает редирект обратно от VK после успешной авторизации.
    Извлекает токен доступа из ответа VK.
    """
    oauth = OAuth2Session(
        client_id, redirect_uri=redirect_uri, state=session['oauth_state'])
    token = oauth.fetch_token(
        'https://oauth.vk.com/access_token',
        authorization_response=request.url,
        client_secret=client_secret
    )
    session.pop('oauth_state', None)
    # Удаляем сохраненное состояние после использования
    return f"Access Token: {token}"


@app.route('/')
def home():
    """
    Главная страница приложения.
    Возвращает простое приветствие.
    """
    return "Привет, мир!"


@app.route('/favicon.ico')
def favicon():
    """
    Маршрут для отправки файла favicon.ico.
    Этот маршрут используется для предоставления браузеру значка
     вкладки (favicon), который отображается рядом с заголовком страницы
    в адресной строке браузера. Файл favicon.ico должен быть размещен
     в папке static вашего Flask приложения.
    Returns:
        Отправляет файл favicon.ico из папки static приложения.
    """
    return send_from_directory(
        app.static_folder,
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


if __name__ == '__main__':
    app.run(debug=True)
