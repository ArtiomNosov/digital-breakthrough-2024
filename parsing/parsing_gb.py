import requests
from bs4 import BeautifulSoup
import fake_useragent
import pickle
import sqlite3
import pandas as pd

def extract_name(content):
    soup = BeautifulSoup(content, 'html.parser')
    title_element = soup.find('title')
    if title_element:
        title = title_element.text.strip()
        return title
    return None

def extract_technologies(content):
    soup = BeautifulSoup(content, 'html.parser')
    technology_elements = soup.find_all('div', class_='promo-tech__item gkb-promo__tag _large ui-text-body--5')
    if not technology_elements:
        technology_elements = soup.find_all('div', class_='gkb-promo__tag-wrapper promo-tech__wrapper')
    if not technology_elements:
        technology_elements = soup.find_all('div', class_='resume-instruments__wrapper')
    if not technology_elements:
        technology_elements = soup.find_all('div', class_='learn-instruments__wrapper')
    if technology_elements:
        technologies = [element.get_text().strip() for element in technology_elements]
        return technologies
    else:
        return None

def save_to_database(name, techs, url):
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses 
                      (id INTEGER PRIMARY KEY,
                       title TEXT,
                       skills TEXT,
                       url TEXT)''')

    cursor.execute('''INSERT INTO vacancies (title, skills,url)
                      VALUES (?, ?, ?)''', (name.lower(), ', '.join(techs).lower(), url))
    conn.commit()
    conn.close()

def delete_url_duplets():
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM courses WHERE id NOT IN (SELECT MIN(id) FROM courses GROUP BY url)''')
    conn.commit()
    conn.close()

def parse_gb_page(url):
    ua = fake_useragent.UserAgent()
    response = requests.get(
        url=url,
        headers={'User-Agent': ua.random}
    )

    if response.status_code == 200:
        content = response.content
        name = extract_name(content)
        techs = extract_technologies(content)
        if not name:
            name = 'Не указано'
        if not techs:
            techs = ['Не указано']
        save_to_database(name, techs, url)
    else:
        return f"Ошибка при загрузке страницы: {response.status_code}"

#url = 'https://gb.ru/geek_university/developer/architecture/network-engineer'
data = pd.read_excel('train_GB_PodborKursov.xlsx', names=['Name', 'Url', 'list'])
url_col = data['Url'].dropna()
urls = url_col.values[2:]
for url in urls:
    parse_gb_page(url)
delete_url_duplets()