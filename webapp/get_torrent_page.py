import requests
from bs4 import BeautifulSoup


def check_login_rutracker():
    username = 'username'
    password = 'password'
    url = 'https://rutracker.appspot.com/forum/login.php'
    sess = requests.Session()
    sess.verify = False
    resp = sess.post(url, data={'username': username, 'password': password})
    resp.raise_for_status()
    resp = sess.get('https://rutracker.appspot.com/forum/viewtopic.php?sid=LE5slP2X&t=5855338')
    resp.raise_for_status()
    print(resp.text)
    return resp.text


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def get_torrent_page(html):
    html = get_html(html)
    html = check_login_rutracker()
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        torrent_news = soup.find('table', id="latest-news-table").findAll('div')
        res_news = []
        for news in torrent_news:
            title = news.find('a').text
            url = news.find('a')['href']
            res_news.append({
                "title": title,
                "url": url,
            })
        return(news)
    return False


if __name__ == "__main__":
    check_login_rutracker()
