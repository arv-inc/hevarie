# 1) Создать Flask проект, добавить в виртуальное окружение BeautifulSoup4
# 2) Создать файл зависимостей используя pip freeze и перенаправление потока
# 3) создать главную страницу, с кнопкой Вход
# 4) Открыть любую страницу торрента (которая доступна) и попробовать спарсить оттуда необходимые данные (название, дату загрузки, какое-нибудь описание)
# 5) по умолчанию главная страница должна выводить эти спарсенные данные (будем потом заменять, главное понять как это работает)
# 6) Сохранять в базу первые три результата по запросу поиска
# 7) Поиск делать сначала в базе – затем на сайте

from flask import Flask, render_template

from webapp.get_torrent_page import get_rutracker_page, parse_torrent_page, parse_search_page
from webapp.forms import RutrackerPage, RutrackerSearch


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    @app.route('/')
    def index():
        page_title = "Hevarie - parser"
        rutracker_form = RutrackerPage()
        rutracker_search = RutrackerSearch()
        return render_template(
            'main_page.html', page_title=page_title, rutracker_form=rutracker_form, rutracker_search=rutracker_search
        )

    @app.route('/search_result', methods=['POST', 'GET'])
    def search_rutracker_page():
        form = RutrackerSearch()
        page_title = "Результат поиска на Rutracker"
        rutracker_login_url = app.config["RUTRACKER_LOGIN_URL"]
        rutracker_login = app.config["RUTRACKER_LOGIN"]
        rutracker_password = app.config["RUTRACKER_PASSWORD"]
        if form.search_text.data:
            search_text = form.search_text.data
            rutracker_search_url = f'https://rutracker.appspot.com/forum/tracker.php?nm={search_text}'
            torrent_url = rutracker_search_url
            search_result = parse_search_page(get_rutracker_page(torrent_url, rutracker_login_url, rutracker_login, rutracker_password))
        else:
            return ("На rutracker.org не найдено")
        if search_result:
            return render_template(
                'search_result.html', search_result=search_result, page_title=page_title, rutracker_search_url=rutracker_search_url
            )
        else:
            return ("Page not found")

    @app.route('/rutracker_page', methods=['POST', 'GET'])
    def parsed_torrent_page():
        torrent_url = "https://rutracker.appspot.com/forum/viewtopic.php?sid=LE5slP2X&t=5855338"
        page_title = "Rutracker Torrent"
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
            return("Rutracker page not found")
            # обработка ошибки при rutracker_page == None

    return app
