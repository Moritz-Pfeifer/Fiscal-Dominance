from splinter import Browser
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import constants
import random
import time
import re
from sqlite3 import Error
import sqlite3


chrome_options = Options()
chrome_options.add_extension('ublock_origin.crx')
browser = Browser('chrome', headless=True, chrome_options=chrome_options)


def db_connect():
    try:
        conn = sqlite3.connect('data.db')
        create_table = """CREATE TABLE IF NOT EXISTS data (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        query TEXT NOT NULL,
                                        title TEXT NOT NULL,
                                        text TEXT NOT NULL,
                                        date_published DATE NOT NULL,
                                        name TEXT NOT NULL
                                        );"""
        conn.execute(create_table)
        return conn
    except Error as e:
        print(e)
    return None


def insert_row(conn, query, title, text, date_published, name):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM data WHERE title = ? AND name = ? AND date_published = ? LIMIT 1", (title, name, date_published))
    if not cur.fetchone():
        conn.execute("INSERT INTO data (query, title, text, date_published, name) VALUES (?, ?, ?, ?, ?);", (query, title, text, date_published, name))
        conn.commit()
        return True


def slumber(min, max):
    time.sleep(random.randint(min, max))


def login():
    url = 'https://acces-distant.sciencespo.fr/fork?https://www.faz-biblionet.de/faz-portal'
    browser.visit(url)
    slumber(1, 3)
    browser.fill('username', constants.username)
    browser.fill('password', constants.password)
    slumber(1, 3)
    browser.find_by_xpath('/html/body/div/div/div[2]/div[1]/form/div[4]/input[4]').click()
    slumber(5, 15)


def click_button(row):
    buttons = row.find_by_css('.hit-link-button')
    for button in buttons:
        article_text = re.sub(r"[\n\t\s]*", "", button.text)
        if article_text == 'Artikel':
            button.click()
            return True


def search(conn, name, institution):
    query = f'{name} AND {institution} NOT Interview'
    url = f'https://www-faz-biblionet-de.acces-distant.sciencespo.fr/faz-portal/faz-archiv?q={query}&DT_from={constants.dt_from}&DT_to={constants.dt_to}'
    browser.visit(url)
    slumber(3, 6)

    cookies_accept = browser.find_by_css('.cb-enable')
    if cookies_accept:
        cookies_accept.click()

    c = 0

    rows = browser.find_by_css('.article-row')
    if len(rows):
        row = rows[0]
        if click_button(row):
            slumber(3, 6)
            while True:
                try:
                    soup = BeautifulSoup(browser.html, 'lxml')
                    if "The system has detected a very high use of electronic resources" in soup.text:
                        input('DAMN! Wait FOR 120mins')
                        soup = BeautifulSoup(browser.html, 'lxml')

                    document = soup.select_one('.single-document')

                    date_published = soup.select_one('.document-article-infos').select('td')[1].text.strip()
                    dd = date_published.split('.')
                    day = dd[0]
                    month = dd[1]
                    year = dd[2]
                    date_published = f'{year}-{day}-{month}'

                    title = document.select_one('pre.docTitle')
                    if title:
                        title = title.text.strip()
                    else:
                        title = f'{name} - {institution} - {date_published}'

                    contents = ''
                    for texts in document.select('pre.text'):
                        contents += texts.text.strip()

                    if insert_row(conn, query, title, contents, date_published, name):
                        c += 1
                        print('count:', c)
                        print('name:', name)
                        print('title:', title)
                        print('date_published:', date_published)
                        print('text:', len(contents))
                        print('-' * 10)
                except Exception as e:
                    print(e)

                next_button = browser.find_by_css('a.next-link')
                if next_button:
                    next_button.first.click()
                    slumber(20, 60)
                else:
                    print('No more articles')
                    return


def main():
    start_time = time.time()

    conn = db_connect()
    login()
    for item in constants.names:
        search(conn, item['name'], item['institution'])
    conn.close()

    end_time = (time.time() - start_time)
    print(f'Execution time in minutes: {end_time / 60}')
    browser.quit()


if __name__ == '__main__':
    main()
