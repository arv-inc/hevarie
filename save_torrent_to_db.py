from webapp import create_app
from webapp.get_rutracker_page import parse_search_result, get_rutracker_page, get_rutracker_session, search_in_db


RUTRACKER_LOGIN_URL = "https://rutracker.org/forum/login.php"
RUTRACKER_SEARCH_URL = "https://rutracker.org/forum/tracker.php?nm=Java"
login = "hevarie"
password = "123456"

headers = {
         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'
        }


app = create_app()
with app.app_context():
    sess = get_rutracker_session(RUTRACKER_LOGIN_URL, login, password)
    parse_search_result(get_rutracker_page(RUTRACKER_SEARCH_URL, sess))
    search_in_db("war")
