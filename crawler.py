import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing.pool import Pool


#variabales
main_url = 'https://coinmarketcap.com'
url_all = 'https://coinmarketcap.com/all/views/all/'

#functions
def get_html(url):
    r = requests.get(url)  # Response
    return r.text  # возвращает Html-код страницы

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('div', class_='cmc-table-listing').find_all('tr', class_='cmc-table-row')
    links = [main_url+td.find('a').get('href') for td in tds]
    return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1').text.strip()
    except:
        name = ''
    try:
        price = soup.find('span', class_='cmc-details-panel-price__price').text.strip()
    except:
        price = ''
    data = {'name': name,
            'price': price}
    return data

def write_csv(data):
    with open('coinmarketcap.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['name'],
                         data['price']))
        print(data['name'], 'parsed')

def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)

def main():
    start = datetime.now()
    all_links = get_all_links(get_html(url_all))

    with Pool(40) as p:
        p.map(make_all, all_links)

    end = datetime.now()
    total = end - start
    print(str(total))

if __name__ == '__main__':
    main()
