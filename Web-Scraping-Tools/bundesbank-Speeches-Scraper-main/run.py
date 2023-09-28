from bs4 import BeautifulSoup
import requests
import constants
import json
import time
import random
from PyPDF2 import PdfReader
import os


def lovely_soup(url):
    r = requests.get(url, cookies=constants.cookies, headers=constants.headers)
    return BeautifulSoup(r.content, 'lxml')


def main():
    query = ''
    per_page = 50
    pages = 9
    date_from = '01.01.2018'
    date_to = '17.04.2023'

    c = 0

    for page in range(0, pages):
        url = f'https://www.bundesbank.de/action/de/729950/bbksearch?hitsPerPageString={per_page}&query={query}&dateTo={date_to}&sort=bbksortdate%20desc&dateFrom={date_from}&pageNumString={page}'
        soup = lovely_soup(url)

        try:
            for item in soup.find_all('li', {'class': 'resultlist__item'}):
                c += 1
                url = item.find('a', {'class': 'teasable__link'})['href']
                if not url.startswith('https://www.bundesbank.de'):
                    url = f'https://www.bundesbank.de{url}'
                title = item.find_all('span', {'class': 'link__label sr-only'})[0].text.strip()
                date = item.find('span', {'class': 'metadata__date'}).text.strip()
                dates = date.split('.')
                d = dates[0]
                m = dates[1]
                y = dates[2]
                date = f'{y}-{m}-{d}'
                author = item.find('span', {'class': 'metadata__authors'}).text.strip().replace('\n', ' ')
                
                if url.endswith('.pdf'):
                    type = 'pdf'
                    r = requests.get(url, headers=constants.headers, cookies=constants.cookies, stream=True)

                    with open(f'file.pdf', 'wb') as f:
                        f.write(r.content)

                    reader = PdfReader(f'file.pdf')
                    number_of_pages = len(reader.pages)
                    content = ''
                    for page in range(0, number_of_pages):
                        content += reader.pages[page].extract_text()
                else:
                    type = 'html'
                    content_soup = lovely_soup(url)
                    main = content_soup.find('main', {'class': 'main'})
                    content = main.find('div', {'class': 'richtext'}).text.strip()

                data = {
                    'url': url,
                    'author': author,
                    'title': title,
                    'date': date,
                    'text': content
                }

                print(c, title, len(content), type)

                with open(f'json/{date}-{c}.json', 'w') as f:
                    json.dump(data, f)

        except Exception as e:
            print(e, url)

        time.sleep(random.randint(2, 5))


if __name__ == '__main__':
    main()
