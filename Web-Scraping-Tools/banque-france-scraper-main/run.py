import constants
import requests
import json
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
from PyPDF2 import PdfReader
import os


def db_connect():
    try:
        conn = sqlite3.connect('data.db')
        create_table = """CREATE TABLE IF NOT EXISTS banque_france (
                                        id integer PRIMARY KEY,
                                        url varchar,
                                        author varchar,
                                        title varchar,
                                        published_date date,
                                        section varchar,
                                        doc_url varchar DEFAULT NULL,
                                        text text DEFAULT NULL
                                        );"""
        conn.execute(create_table)
        return conn
    except Error as e:
        print(e)
    return None


conn = db_connect()


def write_to_db(list_to_db):
    sql = 'INSERT INTO banque_france (url, author, title, published_date, section) VALUES (?,?,?,?,?)'
    conn.execute(sql, (list_to_db))
    conn.commit()


def update_db_one(id, doc_url):
    conn.execute("UPDATE banque_france SET doc_url = ? WHERE ID = ?;", (doc_url, id))
    conn.commit()


def update_db_two(id, text):
    conn.execute("UPDATE banque_france SET text = ? WHERE ID = ?;", (text, id))
    conn.commit()


def select_from_db(query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def lovely_soup(url):
    r = requests.get(url, headers=constants.headers, cookies=constants.cookies)
    return BeautifulSoup(r.content, 'lxml')


def scraper_one():
    keep_sections = ['Discours', 'Interview']

    for page in range(1, 9999):
        params = {
            'selector': 'bdf-page-list-news-form',
            'page': f'{page}',
        }

        response = requests.get(
            'https://www.banque-france.fr/ajax/pagination/news/intervention?selector=bdf-page-list-news-form',
            params=params,
            cookies=constants.cookies,
            headers=constants.headers,
        )

        json_data = response.json()

        for item in json_data:
            if item['command'] == 'insert':
                data = item['data']
                soup = BeautifulSoup(data, 'lxml')
                columns = soup.find_all('div', {'class': 'column-item'})
                if not columns:
                    return
                else:
                    for column in columns:
                        rubriques = column.find('div', {'class': 'rubrique'}).find_all('span')
                        section = rubriques[0].text.strip()
                        author = rubriques[1].text.strip()
                        author = author.split(',')[0].title()
                        title = column.find('h3').text.strip()
                        date = column.find('span', {'class': 'date'}).text.strip().split('/')
                        published_date = f'{date[2]}-{date[1]}-{date[0]}'
                        href = column.find('a', href=True)['href']
                        url = f'https://www.banque-france.fr{href}'
                        if section not in keep_sections:
                            section = 'autres-interventions'
                        print(f'page: {page} |', section, published_date, href)
                        write_to_db([url, author, title, published_date, section])


def scraper_two():
    rows = select_from_db("SELECT ID, url FROM banque_france WHERE doc_url IS NULL")
    for row in rows:
        id = row[0]
        url = row[1]
        soup = lovely_soup(url)
        href = soup.find('a', {'class': 'bdf-share-link--pdf'}, href=True)['href']
        doc_url = url = f'https://www.banque-france.fr{href}'
        print(id, url, doc_url)
        update_db_one(id, doc_url)


def scraper_three():
    rows = select_from_db("SELECT ID, doc_url FROM banque_france WHERE text IS NULL ORDER BY ID ASC")
    for row in rows:
        id = row[0]
        doc_url = row[1]
        try:
            r = requests.get(doc_url, headers=constants.headers, cookies=constants.cookies, stream=True)

            with open(f'file.pdf', 'wb') as f:
                f.write(r.content)

            reader = PdfReader(f'file.pdf')
            number_of_pages = len(reader.pages)
            content = ''
            for page in range(0, number_of_pages):
                content += reader.pages[page].extract_text()
            text = content
            print(id, len(text), doc_url)
            update_db_two(id, text)
            os.remove(f'file.pdf')
        except Exception as e:
            print(doc_url, e)


def export_to_json():
    rows = select_from_db("SELECT ID, doc_url, author, title, text, published_date, section FROM banque_france ORDER BY published_date DESC LIMIT 145")
    for row in rows:
        id = row[0]
        url = row[1]
        author = row[2]
        title = row[3]
        text = row[4]
        published_date = row[5]
        print(published_date)
        section = row[6]
        data = {'url': url, 'author': author, 'title': title, 'text': text, 'published_date': published_date, 'section': section}

        with open(f'json/{section.title()}/{published_date}_{id}.json', 'w+') as f:
            json.dump(data, f)


def main():
    scraper_one()
    scraper_two()
    scraper_three()
    export_to_json()


if __name__ == '__main__':
    main()
