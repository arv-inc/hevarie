# 1) Создать Flask проект, добавить в виртуальное окружение BeautifulSoup4, Requests в виртуальное окружение
# 2) Создать файл зависимостей используя pip freeze и перенаправление потока
# 3) создать главную страницу, с кнопкой Вход
# 4) Открыть любую страницу торрента (которая доступна) и попробовать спарсить оттуда необходимые данные (название, дату загрузки, какое-нибудь описание)
# 5) по умолчанию главная страница должна выводить эти спарсенные данные (будем потом заменять, главное понять как это работает)
from flask import Flask, render_template

from webapp.get_torrent_page import get_rutracker_page, parse_torrent_page


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.route('/')
    def index():
        torrent_url = "https://rutracker.appspot.com/forum/viewtopic.php?sid=LE5slP2X&t=5855338"
        page_title = "Hevarie - parser"
        rutracker_login_url = app.config["RUTRACKER_LOGIN_URL"]
        rutracker_login = app.config["RUTRACKER_LOGIN"]
        rutracker_password = app.config["RUTRACKER_PASSWORD"]
        rutracker_page = parse_torrent_page(get_rutracker_page(torrent_url, rutracker_login_url, rutracker_login, rutracker_password))
        if rutracker_page:
            return render_template(
                'index.html', page_title=page_title,
                rutracker_page=rutracker_page
                )
        else:
            pass
            # обработка ошибки при rutracker_page == None

    return app
