import requests
from bs4 import BeautifulSoup


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
        return(res_news)
    return False


if __name__ == "__main__":
    print(get_torrent_page("https://rutracker.appspot.com/forum/index.php"))
