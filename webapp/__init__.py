# 1) Создать Flask проект, добавить в виртуальное окружение BeautifulSoup4, Requests в виртуальное окружение
# 2) Создать файл зависимостей используя pip freeze и перенаправление потока
# 3) создать главную страницу, с кнопкой Вход
# 4) Открыть любую страницу торрента (которая доступна) и попробовать спарсить оттуда необходимые данные (название, дату загрузки, какое-нибудь описание)
# 5) по умолчанию главная страница должна выводить эти спарсенные данные (будем потом заменять, главное понять как это работает)
from flask import Flask, render_template

from webapp.get_torrent_page import get_html


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.route('/')
    def index():
        page_title = "Hevarie - parser"
        torrent_url = app.config["DEFAULT_TORRENT_URL"]
        torrent_page = get_html(torrent_url)
        return render_template(
            'index.html', page_title=page_title,
            torrent_page=torrent_page
            )

    return app
