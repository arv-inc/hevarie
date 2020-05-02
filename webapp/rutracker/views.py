from flask import Blueprint, render_template
from flask_login import login_required
from webapp.rutracker.models import Torrent4
from webapp.rutracker.forms import RutrackerPage, RutrackerSearch
from webapp.get_rutracker_page import get_html, parse_torrent_page, parse_search_result, get_rutracker_session, search_in_db
from webapp.config import RUTRACKER_LOGIN, RUTRACKER_LOGIN_URL, RUTRACKER_PASSWORD, RUTRACKER_SEARCH_URL

blueprint = Blueprint('rutracker', __name__)

rutracker_session = get_rutracker_session(RUTRACKER_LOGIN_URL, RUTRACKER_LOGIN, RUTRACKER_PASSWORD)


@blueprint.route('/', methods=['POST', 'GET'])
@login_required
def index():
    page_title = "Hevarie - parser"
    rutracker_form = RutrackerPage()
    rutracker_search = RutrackerSearch()
    return render_template(
        'rutracker/main_page.html', page_title=page_title, rutracker_form=rutracker_form, rutracker_search=rutracker_search, sess=rutracker_session
    )


@blueprint.route('/search_result', methods=['POST', 'GET'])
def search_rutracker_page():
    form = RutrackerSearch()
    page_title = "Результат поиска на Rutracker"
    search_text = "%".join(form.search_text.data.split())
    search_result = search_in_db(search_text)
    if not search_result:
        parse_search_result(get_html(f'{RUTRACKER_SEARCH_URL}{search_text}', rutracker_session), rutracker_session)
        search_result = Torrent4.query.filter(Torrent4.torrent_name.ilike(f'%{search_text}%')).all()
    if search_result:
        return render_template(
                'rutracker/three_result.html', search_result=search_result[0:5], page_title=page_title, rutracker_search_url=f'{RUTRACKER_SEARCH_URL}{search_text}'
            )
    else:
        return ("Не найдено")


@blueprint.route('/rutracker_page/', methods=['POST', 'GET'])
def parsed_torrent_page():
    torrent_url = "https://rutracker.org/forum/viewtopic.php?t=5855263"
    page_title = "Rutracker Torrent"
    rutracker_page = parse_torrent_page(get_html(torrent_url, rutracker_session))
    if rutracker_page:
        return render_template(
            'rutracker/index.html', page_title=page_title,
            rutracker_page=rutracker_page
            )
    else:
        return("Rutracker page not found")
