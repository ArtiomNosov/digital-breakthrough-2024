import requests
from bs4 import BeautifulSoup
import fake_useragent
import sqlite3
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd


technology_keywords = ['vue', 'react', 'angular', 'javascript', 
                           'typescript', 'python', 'java', 'c++', 
                           'c#', 'html', 'css', 'sass', 'less', 
                           'bootstrap', 'jquery', 'ajax', 'sql', 
                           'nosql', 'php', 'ruby', 'perl', 'swift', 
                           'kotlin', 'go', 'rust', 'docker', 'kubernetes', 
                           'jenkins', 'git', 'svn', 'node.js', 'express.js', 
                           'flask', 'django', 'spring', 'hibernate', 'android', 
                           'ios', 'mongodb', 'mysql', 'postgresql', 'sqlite', 
                           'oracle', 'aws', 'azure', 'google cloud', 'rest', 
                           'graphql', 'webpack', 'babel', 'gulp', 'npm', 'yarn', 
                           'redux', 'mobx', 'vuex', 'ngrx', 'docker-compose', 
                           'kafka', 'rabbitmq', 'nginx', 'apache', 'linux', 
                           'unix', 'windows', 'macos', 'agile', 'scrum', 'kanban', 
                           'tdd', 'bdd', 'unittest', 'junit', 'pytest', 'selenium', 
                           'cypress', 'jest', 'mocha', 'chai', 'storybook', 'jira', 
                           'confluence', 'gitlab', 'github', 'bitbucket', 'trello', 
                           'slack', 'discord', 'zoom', 'google meet', 'microsoft teams', 
                           'continuous integration', 'continuous deployment',
                           'swift', 'ios', 'android', 'vue.js', 'nuxt', 'tailwindcss']
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def extract_keywords(text):
    tokens = word_tokenize(''.join(text).lower())
    filtered_tokens = [token for token in tokens if token not in stop_words]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    keywords = [token for token in lemmatized_tokens if token in technology_keywords]
    return list(set(keywords))

def extract_experience(description):
    match = re.search(r'Требуемый опыт:\s*(.*?)[,.]', description)
    if match:
        experience_text = match.group(1)
        return experience_text.strip()
    else:
        return None

def extract_skills(content):
    soup = BeautifulSoup(content, 'html.parser')
    skills_element = soup.find_all('div', class_='bloko-tag bloko-tag_inline')
    if skills_element:
        skills = [skill.get_text() for skill in skills_element]
        return skills
    return None
    
def extract_info(content):
    soup = BeautifulSoup(content, 'html.parser')
    title_element = soup.find('title')
    if title_element:
        title = title_element.text.strip()
        return title
    return None
    
def extract_description(content):
    soup = BeautifulSoup(content, 'html.parser')
    description_element = soup.find('meta', {'name': 'description'})
    if description_element:
        vacancy_description = description_element['content']
        return vacancy_description
    return None

def extract_main(content):
    soup = BeautifulSoup(content, 'html.parser')
    expectations_elements = soup.find_all(['ul', 'li', 'p'])
    main_elements = []
    if expectations_elements:
        for element in expectations_elements:
            main_elements.append(element.text.strip())
        return main_elements
    return None
    
def save_to_database(info, description, experience, skills, main, url, keywords):
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS vacancies 
                      (id INTEGER PRIMARY KEY,
                       title TEXT,
                       description TEXT,
                       experience TEXT,
                       skills TEXT,
                       main_requirements TEXT,
                       main_text TEXT,
                       url TEXT)''')

    cursor.execute('''INSERT INTO vacancies (title, description, experience, skills, main_requirements, main_text,url)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (info.lower(), description.lower(), experience.lower(), ', '.join(skills).lower(), ', '.join(keywords).lower(), ', '.join(main).lower(), url))
    conn.commit()
    conn.close()

def delete_url_duplets():
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM vacancies WHERE id NOT IN (SELECT MIN(id) FROM vacancies GROUP BY url)''')
    conn.commit()
    conn.close()

def parse_vacancy_page(url):
    ua = fake_useragent.UserAgent()
    response = requests.get(
        url=url,
        headers={'User-Agent': ua.random}
    )

    if response.status_code == 200:
        content = response.content
        skills = extract_skills(content)
        info = extract_info(content)
        description = extract_description(content)
        experience = extract_experience(description)
        main = extract_main(content)
        keywords = extract_keywords(main)

        if not skills:
            skills = ['Не указано']
        if not info:
            info = 'Не указано'
        if not description:
            description = 'Не указано'
        if not main:
            main = ['Не указано']
        if not experience:
            experience = 'Не указано'
        if not keywords:
            keywords = ['Не указано']
        save_to_database(info, description, experience, skills, main, url, keywords)
    else:
        return f"Ошибка при загрузке страницы: {response.status_code}"

#url = 'https://hh.ru/vacancy/94780591'
data = pd.read_excel('train_GB_PodborKursov.xlsx', names=['Name', 'Url', 'list'])
list_col = data['list'].dropna()
urls = list_col.values[1:]
for url in urls:
    parse_vacancy_page(url)
delete_url_duplets()