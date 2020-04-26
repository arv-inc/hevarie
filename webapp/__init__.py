# 1) Создать Flask проект, добавить в виртуальное окружение BeautifulSoup4
# 2) Создать файл зависимостей используя pip freeze и перенаправление потока
# 3) создать главную страницу, с кнопкой Вход
# 4) Открыть любую страницу торрента (которая доступна) и попробовать спарсить оттуда необходимые данные (название, дату загрузки, какое-нибудь описание)
# 5) по умолчанию главная страница должна выводить эти спарсенные данные (будем потом заменять, главное понять как это работает)
# 6) Сохранять в базу первые три результата по запросу поиска
# 7) Поиск делать сначала в базе – затем на сайте

from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from webapp.model import db, Torrent, User
from webapp.get_rutracker_page import get_rutracker_page, parse_torrent_page, parse_search_result, get_rutracker_session
from webapp.forms import RutrackerPage, RutrackerSearch, LoginForm


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    rutracker_login_url = app.config["RUTRACKER_LOGIN_URL"]
    rutracker_login = app.config["RUTRACKER_LOGIN"]
    rutracker_password = app.config["RUTRACKER_PASSWORD"]
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    try:
        sess = get_rutracker_session(rutracker_login_url, rutracker_login, rutracker_password)
    except(ValueError):
        return("Ошибка сети")

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    @login_required
    def index():
        page_title = "Hevarie - parser"
        rutracker_form = RutrackerPage()
        rutracker_search = RutrackerSearch()
        return render_template(
            'main_page.html', page_title=page_title, rutracker_form=rutracker_form, rutracker_search=rutracker_search, sess=sess
        )

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли на сайт Hevarie')
                return redirect(url_for('index'))
        flash('Неправильное имя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно вышли')
        return redirect(url_for('login'))

    @app.route('/search_result', methods=['POST', 'GET'])
    def search_rutracker_page():
        form = RutrackerSearch()
        page_title = "Результат поиска на Rutracker"
        rutracker_search_url = app.config["RUTRACKER_SEARCH_URL"]
        search_text = form.search_text.data
        rutracker_search_url = f'{rutracker_search_url}{search_text}'
        search_result = Torrent.query.filter(Torrent.torrent_name.ilike(f'%{search_text}%')).all()
        if not search_result:
            parse_search_result(get_rutracker_page(rutracker_search_url, sess))
            search_result = Torrent.query.filter(Torrent.torrent_name.ilike(f'%{search_text}%')).all()
        else:
            pass
        if search_result:
            return render_template(
                    'three_result.html', search_result=search_result, page_title=page_title, rutracker_search_url=rutracker_search_url
                )
        else:
            return ("Не найдено")

    @app.route('/rutracker_page', methods=['POST', 'GET'])
    def parsed_torrent_page():
        torrent_url = "https://rutracker.org/forum/viewtopic.php?sid=LE5slP2X&t=5855338"
        page_title = "Rutracker Torrent"
        rutracker_page = parse_torrent_page(get_rutracker_page(torrent_url, sess))
        if rutracker_page:
            return render_template(
                'index.html', page_title=page_title,
                rutracker_page=rutracker_page
                )
        else:
            return("Rutracker page not found")
    return app
