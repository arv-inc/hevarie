import requests
from bs4 import BeautifulSoup


def get_rutracker_page(html_url, login_page_url, username, password):
    try:
        sess = requests.Session()
        sess.verify = False
        resp = sess.post(login_page_url, data={'login_username': username, 'login_password': password, "login": "login"})
        resp = sess.get(html_url)
        resp.raise_for_status()
        return resp.text
    except(requests.RequestException, ValueError):
        return(False, "Сетевая ошибка")


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def parse_torrent_page(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            torrent_added = soup.find('a', class_='p-link small').text
            torrent_since = soup.find('span', class_='posted_since hide-for-print').text
            torrent_description = soup.find('div', class_="post_body")
            created_by = f'Производитель{torrent_description.find(string="Производитель").next}'
            creater_url = f'Сайт производителя: {torrent_description.find("a", class_="postLink")["href"]}'
            creater_name = f'Автор{torrent_description.find(string="Автор").next}'
            torrent_short_description = f'Описание{torrent_description.find(string="Описание").next}'  # Не получилось взять описание с нового абзаца
            torrent_title = torrent_description.find('span').text
        except (TypeError, AttributeError):
            print("Описание не найдено")
            return None

        torrent_description_list = {'torrent_added': torrent_added,
                                    'torrent_since': torrent_since,
                                    'torrent_title': torrent_title,
                                    'created_by': created_by,
                                    'creater_url': creater_url,
                                    'creater_name': creater_name,
                                    'torrent_short_description': torrent_short_description
                                    }
        return(torrent_description_list)
    return False
