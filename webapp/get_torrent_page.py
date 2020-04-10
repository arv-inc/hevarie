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
    headers = {
         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'
        }
    try:
        result = requests.get(url, headers) # Sessions -???
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def parse_search_page(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            torrent_group = soup.find('a', class_='gen f ts-text').text
            torrent_name = soup.find('a', class_='med tLink ts-text hl-tags bold').text
            torrent_created = soup.find('td', class_='row4 small nowrap').text
            # torrent_tag = soup.find('div', class_='t-tags')  # может отсутсtorrent_size = soup.find('a', class_='gr-button tr-dl dl-stub').text
            torrent_link = soup.find('a', class_='small tr-dl dl-stub')['href']
            torrent_size = soup.find('a', class_='small tr-dl dl-stub').text
        except (TypeError, AttributeError):
            print("По данному запросу ничего нет")
            return None

        search_result_dict = {'torrent_group': torrent_group,
                              'torrent_name': torrent_name,
                              'torrent_created': torrent_created,
                            #  'torrent_tag': torrent_tag
                               'torrent_size': torrent_size,
                               'torrent_link': torrent_link
                             }
        return search_result_dict
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


if __name__ == "__main__":
    # print(get_rutracker_page(
    #             'https://rutracker.appspot.com/forum/tracker.php?nm=python',
    #             'https://rutracker.appspot.com/forum/login.php',
    #             'hevarie',
    #             '123456'
    #             )
    #             )

    print(parse_search_page(get_rutracker_page(
                'https://rutracker.appspot.com/forum/tracker.php?nm=python',
                'https://rutracker.appspot.com/forum/login.php',
                'hevarie',
                '123456'
                )
                )
                )
