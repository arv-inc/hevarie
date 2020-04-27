from datetime import datetime

import requests
from webapp.rutracker.models import db, Torrent
from bs4 import BeautifulSoup
from webapp.config import headers


def get_rutracker_session(login_page_url, username, password):
    try:
        session = requests.Session()
        session.verify = False
        session.post(login_page_url, data={'login_username': username, 'login_password': password, "login": "login"}, headers=headers)
    except(ValueError):
        return("Ошибка сети")
    return(session)


def get_rutracker_page(html_url, sess):
    try:
        resp = sess.get(html_url)
        resp.raise_for_status()
        return resp.text
    except(ValueError):
        return(False, "Сетевая ошибка")


def get_html(url):
    try:
        result = requests.get(url, headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def get_proxy():
    url = 'https://free-proxy-list.net/'
    try:
        proxy_page = get_html(url)
    except(ValueError):
        return("Сетевая ошибка")
    soup = BeautifulSoup(proxy_page, 'html.parser')
    try:
        proxy_list = soup.find('tbody').findAll('tr')
        for proxy in proxy_list:
            proxy_ip = proxy.find('td').text
            proxy_port = proxy.find('td').next.next.text
            proxies = {
                        'http': f'http://{proxy_ip}:{proxy_port}',
                        'https': f'http://{proxy_ip}:{proxy_port}',
                    }
            try:
                print(proxy_ip, proxy_port)
                request = requests.post('https://rutracker.org/forum/login.php', proxies=proxies)
                print(request.status_code())
            except(ValueError):
                print("сетевая ошибка")
    except(TypeError, AttributeError):
        print("Прокси не найдены")
        return None
    return proxy_ip


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


def parse_search_result(html):
    # three_torrent_list = []
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            torrent_group = soup.find('tbody').findAll('tr', class_="tCenter hl-tr")
        except (TypeError, AttributeError):
            print("По данному запросу ничего нет")
            return None
        for torrent in torrent_group[0:3]:
            torrent_name = torrent.find('a', class_='med tLink ts-text hl-tags bold').text
            torrent_date = torrent.find('td', class_='row4 small nowrap').text
            try:
                torrent_date = datetime.strptime(torrent_date, '%d-%m-%Y')
            except ValueError:
                torrent_date = datetime.now()
            torrent_size = torrent.find('a', class_='small tr-dl dl-stub').text
            torrent_link = torrent.find('a', class_='small tr-dl dl-stub')['href']
    #         three_torrent_dict = {
    #             'torrent_name': torrent_name,
    #             'torrent_created': torrent_date,
    #             'torrent_size': torrent_size,
    #             'torrent_download_link': f'https://rutracker.org/forum/{torrent_link}'
    #         }
    #         three_torrent_list.append(three_torrent_dict)
    #     return three_torrent_list
            save_torrent(torrent_name, torrent_date, torrent_size, torrent_link)
        return True
    return False


def save_torrent(torrent_name, torrent_date, torrent_size, torrent_file_link):
    new_torrent = Torrent(torrent_name=torrent_name, torrent_date=torrent_date, torrent_size=torrent_size, torrent_file_link=torrent_file_link)
    db.session.add(new_torrent)
    db.session.commit()


if __name__ == "__main__":

    print(get_rutracker_session())
