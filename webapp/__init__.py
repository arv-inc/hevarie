# 1) Создать Flask проект, добавить в виртуальное окружение BeautifulSoup4
# 2) Создать файл зависимостей используя pip freeze и перенаправление потока
# 3) создать главную страницу, с кнопкой Вход
# 4) Открыть любую страницу торрента (которая доступна) и попробовать спарсить оттуда необходимые данные (название, дату загрузки, какое-нибудь описание)
# 5) по умолчанию главная страница должна выводить эти спарсенные данные (будем потом заменять, главное понять как это работает)
# 6) Сохранять в базу первые три результата по запросу поиска
# 7) Поиск делать сначала в базе – затем на сайте
# 8) Добавить описание к торренту
# убрать лишнее в названии
# 9) задеплойть

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.user.views import blueprint as user_blueprint
from webapp.user.models import Tuser as User
from webapp.rutracker.views import blueprint as rutracker_blueprint
from webapp.db import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(user_blueprint)
    app.register_blueprint(rutracker_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
