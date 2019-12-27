import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)  # Response
    return r.text  # возвращает Html-код страницы


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('div', class_='cmc-table-listing').find_all('tr', class_='cmc-table-row')
    links = [td.find('a').get('href') for td in tds]
    return links


def main():
    url = 'https://coinmarketcap.com'
    url_all = 'https://coinmarketcap.com/all/views/all/'
    all_links = get_all_links(get_html(url_all))

    for i in all_links:
        print(url+i)

if __name__ == '__main__':
    main()