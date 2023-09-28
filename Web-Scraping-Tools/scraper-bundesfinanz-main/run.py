from bs4 import BeautifulSoup
import requests
import json
import constants
import wayback
from wayback import Mode
import datetime
import sqlite3
from sqlite3 import Error


def db_connect():
    try:
        conn = sqlite3.connect('data.db')
        create_table = """CREATE TABLE IF NOT EXISTS data (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        url TEXT NULL,
                                        title TEXT NULL,
                                        author TEXT NULL,
                                        published_date TEXT NULL,
                                        content TEXT NULL
                                        );"""
        conn.execute(create_table)
        return conn
    except Error as e:
        print(e)
    return None


conn = db_connect()
wayback_client = wayback.WaybackClient()


def insert_row(url, title, author, date, content):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM data WHERE url = ? LIMIT 1", (url,))
    if not cur.fetchone():
        conn.execute("INSERT INTO data (url, title, author, published_date, content) VALUES (?, ?, ?, ?, ?);", (url, title, author, date, content))
        conn.commit()
        print(url + ' Added to db')
    else:
        print(url + ' Already exists in db')


def update_row(id, content):
    conn.execute(f"UPDATE data SET content = ? WHERE ID = ?", (content, id))
    conn.commit()
    print(f'{id} Updated in db')


def lovely_soup(url):
    r = requests.get(url, headers=constants.headers, cookies=constants.cookies)
    return BeautifulSoup(r.content, 'lxml')


def scraper_one():
    pages = 10
    c = 0

    for page in range(1, pages + 1):
        soup1 = lovely_soup(f'https://www.bundesfinanzministerium.de/Web/DE/Presse/RedenUndInterviews/redenUndInterviews.html?gtp=%2526e7f1c246-e4ad-4de6-8ad0-505f75d38e6b_list%253D{page}')

        results = soup1.find('ol', {'id': 'searchResult'})
        items = results.find_all('li', {'class': 'bmf-list-entry'})
        for item in items:
            c += 1
            link = item.find('a', href=True)
            url = 'https://www.bundesfinanzministerium.de' + link['href']
            title = link.text.strip()
            date = item.find('time')['datetime'].split('T')[0]

            soup2 = lovely_soup(url)
            content_wrapper = soup2.find('div', {'class': 'article-text'})
            datum = content_wrapper.find('ul', {'class': 'doc-data'})
            if datum:
                datum = datum.text
            else:
                datum = ''
            content = content_wrapper.text.replace(datum, '').strip()
            author = None
            authors = []

            for expected_author in constants.expected_authors:
                if expected_author in content:
                    authors.append(expected_author)
            if authors:
                author = ', '.join(authors)

            insert_row(url, title, author, date, content)

            #if len(content):
            #    with open(f'json/{date}-{c}.json', 'w') as f:
            #        json.dump(data, f)


def scraper_two():
    pages = 10
    c = 0

    for page in range(1, pages + 1):
        for record in wayback_client.search(f'https://www.bundesfinanzministerium.de/Web/DE/Presse/RedenUndInterviews/redenUndInterviews.html?gtp=%2526e7f1c246-e4ad-4de6-8ad0-505f75d38e6b_list%253D{page}', match_type='exact'):
            url = record[-1]
            try:
                response = wayback_client.get_memento(record, mode=Mode.original)
                content = response.content

                soup = BeautifulSoup(content, 'lxml')
                results = soup.find('ol', {'id': 'searchResult'})
                if results:
                    items = results.find_all('li', {'class': 'bmf-list-entry'})
                    if items:
                        for item in items:
                            link = item.find('a', href=True)
                            span = link.find('span', {'class': 'bmf-labelbox-text'})
                            url = 'https://www.bundesfinanzministerium.de' + link['href']
                            title = link.text
                            if span:
                                title = title.replace(span.text, '')
                            title = title.replace('\n', '').strip(' \t\n\r')
                            date = item.find('time')['datetime'].split('T')[0]
                            year = date.split()
                            insert_row(url, title, None, date, None)
            except Exception as e:
                pass
                #print(e)


def scraper_three():
    cur = conn.cursor()
    cur.execute("SELECT ID, url FROM data WHERE content IS NULL")
    rows = cur.fetchall()
    for row in rows:
        id = row[0]
        url = row[1]

        for record in wayback_client.search(url, match_type='exact'):
            url = record[-1]
            #print(url)
            try:
                response = wayback_client.get_memento(record, mode=Mode.original)
                content = response.content
                soup = BeautifulSoup(content, 'lxml')
                content_wrapper = soup.find('div', {'class': 'article-text'})
                datum = content_wrapper.find('ul', {'class': 'doc-data'})
                if datum:
                    datum = datum.text
                else:
                    datum = ''
                text_content = content_wrapper.text.replace(datum, '').strip()
                #print(text_content)
                update_row(id, text_content)
                break
            except Exception as e:
                print(e)
                pass

def writer():
    cur = conn.cursor()
    cur.execute("SELECT * FROM data WHERE content IS NOT NULL AND published_date > 2017")
    rows = cur.fetchall()
    for row in rows:
        data = {
            'url': row[1],
            'author': row[3],
            'title': row[2],
            'published_date': row[4],
            'text': row[5]
        }

        with open(f'json/{row[4]}-{row[0]}.json', 'w') as f:
            json.dump(data, f)

def main():
    scraper_one()
    scraper_two()
    scraper_three()
    writer()

if __name__ == '__main__':
    main()
