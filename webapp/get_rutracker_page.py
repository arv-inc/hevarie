from datetime import datetime
import locale
import platform

from sqlalchemy.exc import IntegrityError, InvalidRequestError
import requests
from webapp.rutracker.models import db, Torrent4
from bs4 import BeautifulSoup
from webapp.config import headers

if platform.system() == "Windows":
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")


def get_rutracker_session(login_page_url, username, password):
    try:
        session = requests.Session()
        session.verify = False
        session.post(login_page_url, data={'login_username': username, 'login_password': password, "login": "login"}, headers=headers)
    except(ValueError):
        return("Ошибка сети")
    return(session)


def get_html(html_url, sess):
    try:
        resp = sess.get(html_url)
        resp.raise_for_status()
        return resp.text
    except(ValueError):
        return(False, "Сетевая ошибка")


def parse_torrent_page(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            torrent_added = soup.find('a', class_='p-link small').text
        except (TypeError, AttributeError):
            torrent_added = "отсутсвует"
        try:
            torrent_since = soup.find('span', class_='posted_since hide-for-print').text
        except (TypeError, AttributeError):
            torrent_since = "отсутсвует"
        try:
            torrent_description = soup.find('div', class_="post_body")
        except (TypeError, AttributeError):
            torrent_description = "отсутсвует"
        try:
            created_by = f'Производитель{torrent_description.find(string="Производитель").next}'
        except (TypeError, AttributeError):
            created_by = "отсуствует"
        try:
            creater_url = torrent_description.find("a", class_="postLink")["href"]
        except (TypeError, AttributeError):
            creater_url = "отсутствует"
        try:
            creater_name = f'Автор{torrent_description.find(string="Автор").next}'
        except (TypeError, AttributeError):
            creater_name = "не указан"
        try:
            torrent_short_description = f'Описание{torrent_description.find(string="Описание").next}'  # Не получилось взять описание с нового абзаца
        except (TypeError, AttributeError):
            torrent_short_description = "отсутствует"
        try:
            torrent_title = torrent_description.find('span').text
        except (TypeError, AttributeError):
            torrent_title = "Описание не найдено"

        torrent_description_dict = {'torrent_added': torrent_added,
                                    'torrent_since': torrent_since,
                                    'torrent_title': torrent_title,
                                    'created_by': created_by,
                                    'creater_url': creater_url,
                                    'creater_name': creater_name,
                                    'torrent_short_description': torrent_short_description
                                    }
        return(torrent_description_dict)
    return False


def parse_search_result(html, sess):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            torrent_group = soup.find('tbody').findAll('tr', class_="tCenter hl-tr")
        except (TypeError, AttributeError):
            print("По данному запросу ничего нет")
            return None
        count = 0
        for torrent in torrent_group:
            try:
                torrent_name = torrent.find('a', class_='med tLink ts-text hl-tags bold').text
            except AttributeError:
                continue
            torrent_date = torrent.find('td', class_='row4 small nowrap').text
            try:
                torrent_date = datetime.strptime(' '.join(torrent_date[1:10].split('-')), '%d %b %y')
            except ValueError:
                torrent_date = datetime.now()
            torrent_size = torrent.find('a', class_='small tr-dl dl-stub').text
            torrent_link = f"https://rutracker.org/forum/{torrent.find('a', class_='med tLink ts-text hl-tags bold')['href']}"
            torrent_download_link = f"https://rutracker.org/forum/{torrent.find('a', class_='small tr-dl dl-stub')['href']}"
            torrent_description = (get_html(torrent_link, sess))
            save_torrent(torrent_name, torrent_date, torrent_size, torrent_link, torrent_download_link, torrent_description)
            count += 1
            if count == 10:
                break
        return True
    return False


def save_torrent(torrent_name, torrent_date, torrent_size, torrent_link, torrent_download_link, torrent_description):
    torrent_exist_count = Torrent4.query.filter(Torrent4.torrent_download_link == torrent_download_link).count()
    print(torrent_exist_count)
    if not torrent_exist_count:
        new_torrent = Torrent4(
            torrent_name=torrent_name,
            torrent_date=torrent_date,
            torrent_size=torrent_size,
            torrent_link=torrent_link,
            torrent_download_link=torrent_download_link,
            torrent_description=torrent_description
            )
        try:
            db.session.add(new_torrent)
            db.session.commit()
        except (IntegrityError, InvalidRequestError):
            print(f'{torrent_name}: "Already saved"')
            return("Already saved")


def search_in_db(search_text):
    search_in_db_result = Torrent4.query.filter(Torrent4.torrent_name.ilike(f'%{search_text}%')).all()
    if len(search_in_db_result) > 5:
        return search_in_db_result
    else:
        return False


def search_link(search_text, sess):
    link = Torrent4.query.filter(Torrent4.id == search_text).first().torrent_link
    torrent_description = parse_torrent_page(get_html(link, sess))
    return torrent_description


if __name__ == "__main__":
    search_in_db()
