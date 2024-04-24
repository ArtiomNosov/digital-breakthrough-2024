import dateparser
from transformers import pipeline
import datetime
from datetime import timedelta
import re
import nltk
from pymystem3 import Mystem
import pymorphy3
from nltk.stem.snowball import SnowballStemmer
import re
nltk.download('punkt')
#from utils import (normalize_station_name,
#                   lemmatize_sentence,
#                   translate_date,
#                   change_weird_words_to_normal,
#                   words_to_numbers,
#                   split_hyphenated_words)
from dataclasses import dataclass


@dataclass
class Variables:
    DCT_NUMBERS_ADJ = {
        'первый': 1,
        'второй': 2,
        'третий': 3,
        'четвёртый': 4,
        'пятый': 5,
        'шестой': 6,
        'седьмой': 7,
        'восьмой': 8,
        'девятый': 9,
        'десятый': 10,
        'одиннадцатый': 11,
        'двенадцатый': 12,
        'тринадцатый': 13,
        'четырнадцатый': 14,
        'пятнадцатый': 15,
        'шестнадцатый': 16,
        'семнадцатый': 17,
        'восемнадцатый': 18,
        'девятнадцатый': 19,
        'двадцатый': 20,
        'тридцатый': 30,
    }
    NUMBERS_DICT = {
        'один': 1,
        'два': 2,
        'три': 3,
        'четыре': 4,
        'пять': 5,
        'шесть': 6,
        'семь': 7,
        'восемь': 8,
        'девять': 9,
        'десять': 10,
        'одиннадцать': 11,
        'двенадцать': 12,
        'тринадцать': 13,
        'четырнадцать': 14,
        'пятнадцать': 15,
        'шестнадцать': 16,
        'семнадцать': 17,
        'восемнадцать': 18,
        'девятнадцать': 19,
        'двадцать': 20,
        'двадцать один': 21,
        'двадцать два': 22,
        'двадцать три': 23,
        'двадцать четыре': 24,
        'двадцать пять': 25,
        'двадцать шесть': 26,
        'двадцать семь': 27,
        'двадцать восемь': 28,
        'двадцать девять': 29,
        'тридцать': 30,
        'тридцать один': 31
    }
    MONTHS_DICT = {
        'январь': '01',
        'февраль': '02',
        'март': '03',
        'апрель': '04',
        'май': '05',
        'июнь': '06',
        'июль': '07',
        'август': '08',
        'сентябрь': '09',
        'октябрь': '10',
        'ноябрь': '11',
        'декабрь': '12'
    }
    STATIONS = [ "Яхромская", "Ясенево", "Южная", "Юго-Западная", "Юго-Восточная",
    "Электрозаводская", "Щукинская", "Щёлковская", "Шоссе Энтузиастов",    "Шипиловская", "Шелепиха", "Шаболовская", "Чкаловская", "Чистые пруды",
    "Чеховская", "Чертановская", "Черкизовская", "ЦСКА", "Цветной Бульвар",    "Царицыно", "Хорошёвская", "Хорошевская", "Хорошёво", "Ховрино",
    "Фрунзенская", "Фонвизинская", "Фили", "Филёвский парк", "Филатов луг",    "Физтех", "Университет", "Улица Скобелевская", "Улица Дмитриевского",
    "Улица Горчакова", "Улица Академика Янгеля", "Улица 1905 года",    "Угрешская", "Тушинская", "Тургеневская", "Тульская", "Трубная",
    "Тропарёво", "Третьяковская", "ТПУ Рязанская", "Тимирязевская",    "Технопарк", "Терехово", "Тёплый стан", "Текстильщики", "Театральная",
    "Тверская", "Таганская", "Сходненская", "Сухаревская", "Студенческая",    "Строгино", "Стрешнево", "Стенд", "Станционная", "Старокачаловская",
    "Сретенский Бульвар", "Спортивная", "Спартак", "Солнцево", "Сокольники",    "Соколиная Гора", "Сокол", "Смоленская", "Славянский бульвар",
    "Серпуховская", "Семёновская", "Селигерская", "Севастопольская",    "Свиблово", "Саларьево", "Савёловская", "Рязанский Проспект",
    "Румянцево", "Ростокино", "Римская", "Рижская", "Речной вокзал",    "Рассказовка", "Раменки", "Пятницкое шоссе", "Пыхтино", "Пушкинская",
    "Профсоюзная", "Проспект Мира", "Проспект Вернадского", "Пролетарская",    "Прокшино", "Преображенская площадь", "Пражская", "Полянка",
    "Полежаевская", "Площадь Революции", "Площадь Ильича", "Площадь Гагарина",    "Планерная", "Пионерская", "Печатники", "Петровско-Разумовская",
    "Петровский парк", "Перово", "Первомайская", "Партизанская", "Парк Победы",    "Парк культуры", "Панфиловская", "Павелецкая", "Охотный ряд", "Отрадное",
    "Орехово", "Ольховая", "Октябрьское поле", "Октябрьская", "Окская",    "Окружная", "Озёрная", "Новые Черёмушки", "Новоясеневская", "Новохохловская",
    "Новослободская", "Новопеределкино", "Новокузнецкая", "Новокосино",    "Новогиреево", "Новаторская", "Нижегородская", "Некрасовка",
    "Нахимовский Проспект", "Народное Ополчение", "Нагорная", "Нагатинский затон",    "Нагатинская", "Мякинино", "Москва-Сити", "Молодёжная", "Мнёвники",
    "Мичуринский проспект", "Митино", "Минская", "Менделеевская", "Медведково",    "Маяковская", "Марьино", "Марьина Роща", "Марксистская", "Люблино",
    "Лухмановская", "Лужники", "Лубянка", "Ломоносовский проспект",    "Ломоносовский проспект", "Локомотив", "Лихоборы", "Лианозово", "Лефортово",
    "Лесопарковая", "Лермонтовский проспект", "Ленинский Проспект",    "Кутузовская", "Курская", "Кунцевская", "Кузьминки", "Кузнецкий мост",
    "Крымская", "Крылатское", "Кропоткинская", "Крестьянская застава",    "Красные ворота", "Красносельская", "Краснопресненская", "Красногвардейская",
    "Котельники", "Косино", "Коптево", "Коньково", "Комсомольская", "Коммунарка",    "Коломенская", "Кожуховская", "Кленовый бульвар", "Китай-город", "Киевская",
    "Каширская", "Каховская", "Кантемировская", "Калужская", "Измайловская",    "Измайлово", "Зябликово", "Зюзино", "Зорге", "ЗИЛ", "Жулебино", "Дубровка",
    "Достоевская", "Домодедовская", "Добрынинская", "Дмитровская", "Динамо",    "Деловой центр", "Давыдково", "Говорово", "Выхино", "Воронцовская",
    "Воробьёвы горы", "Волоколамская", "Волжская", "Волгоградский проспект",    "Войковская", "Водный Стадион", "Владыкино", "Верхние Лихоборы",
    "Верхние Котлы", "ВДНХ", "Варшавская", "Бутырская", "Бунинская аллея",    "Бульвар Рокоссовского", "Бульвар Дмитрия Донского", "Бульвар Адмирала Ушакова",
    "Братиславская", "Ботанический сад", "Боровское шоссе", "Боровицкая",    "Борисово", "Битцевский парк", "Библиотека имени Ленина", "Бибирево",
    "Беляево", "Белорусская", "Беломорская", "Белокаменная", "Беговая",    "Бауманская", "Баррикадная", "Балтийская", "Багратионовская", "Бабушкинская",
    "Аэропорт Внуково", "Аэропорт", "Арбатская", "Аннино", "Андроновка",    "Аминьевская", "Алтуфьево", "Алма-Атинская", "Алексеевская",
    "Александровский сад", "Академическая", "Административная", "Автозаводская", "Авиамоторная"]
    PATTERN = r'\b(?:\d{1,2}\s+\w+|\d{1,2}\s+\w+\s+\d{4}|следующий\s+\w+|назад\s+\d+\s+\w+|через\s+\d+\s+\w+)\b'
    HALF = {
        'Полторы': 1.5,
        'Полтора': 1.5,
        'Две с половиной': 2.5,
        'Два с половиной': 2.5,
        'Три с половиной': 3.5,
    }
    QUESTION_DATE = 'Выдели все, что связано с датой'
    QUESTION_STATION = 'Какая станция метро?'
    DCT_OF_WEIRDS = {
        'пару': '2',
        'тройку': '3'
    }



stemmer = SnowballStemmer("russian")
morph = pymorphy3.MorphAnalyzer()
mystem = Mystem()


def lemmatize_sentence(text: str) -> str:
    lemmas = mystem.lemmatize(text)
    return ' '.join(lemmas).strip()


def get_station_name(text, stations):  # МЕНЯЛ
    text = text.lower().split()

    for station in stations:
      counter = 0
      words_to_delete = []
      for i in range(len(text)):
        for station_el in station.lower().split():
          if morph.parse(text[i])[0].normal_form == morph.parse(station_el)[0].normal_form:
            words_to_delete.append(text[i])
            counter += 1

      if counter == len(station.split()):
        return station, words_to_delete
      else:
        continue

    return 'Incorrect request'


def translate_date(text):  # МЕНЯЛ
    words = [morph.parse(word)[0].normal_form for word in text.lower().split()]
    result = []
    for i in range(len(words)):
        if words[i] in Variables.MONTHS_DICT:
            if words[i-1].isdigit():
                day = words[i-1].zfill(2)
                month = Variables.MONTHS_DICT[words[i]]
                year = '2024'
                result = words[:i-1] + [f"{day}.{month}.{year}"]
        else:
          result += [words[i]]

    return ' '.join(result)


def sum_numbers_in_text(text: str) -> str:
    pattern = r'\b(\d+)\s(\d+)\b'

    def add_nums(match) -> str:
        num1, num2 = match.groups()
        result = int(num1) + int(num2)
        return str(result)

    result = re.sub(pattern, add_nums, text)
    return result


def words_to_numbers(text: str) -> str:
    words = text.split()
    for i, word in enumerate(words):
        parsed_word = morph.parse(word)[0]
        if 'NUMR' in parsed_word.tag:
            words[i] = str(Variables.NUMBERS_DICT[parsed_word.normal_form])
        elif parsed_word.normal_form in Variables.DCT_NUMBERS_ADJ.keys():
            words[i] = str(Variables.DCT_NUMBERS_ADJ[parsed_word.normal_form])
    return sum_numbers_in_text(' '.join(words))


def change_weird_words_to_normal(text: str) -> str:
    words = text.split()
    for key in Variables.DCT_OF_WEIRDS.keys():
        for i in range(len(words)):
            if key == words[i]:
                words[i] = Variables.DCT_OF_WEIRDS[key]
    return ' '.join(words)


def split_hyphenated_words(text: str) -> str:
    words = text.split('-')
    new_text = ' - '.join(words)
    return new_text


def check_weekday_in_text(text: str) -> str: # ДОБАВИЛ
    weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    for weekday in weekdays:
        if re.search(weekday, text, re.IGNORECASE):
            ind = re.search(weekday, text, re.IGNORECASE).span()
            return True, text[ind[0]:ind[1]]
    return False


def change_day_of_week(date_str: str, day_name: str): # ДОБАВИЛ
    weekdays = {
      'понедельник': 0,
      'вторник': 1,
      'среда': 2,
      'четверг': 3,
      'пятница': 4,
      'суббота': 5,
      'воскресенье': 6
    }
    date = datetime.strptime(date_str, '%Y-%m-%d')
    changed_day = date - timedelta(days=date.weekday()) + timedelta(days=weekdays[day_name])

    return changed_day.strftime('%Y-%m-%d')


model_pipeline = pipeline(
    task='question-answering',
    model='timpal0l/mdeberta-v3-base-squad2'
)


class MetroDataExtractor:
    def __init__(self):
        pass

    def process_list_to_strings(self, tokens: list) -> str:
        return ' '.join(tokens)

    def extract_station(self, text: str) -> str:
        answer = model_pipeline(question=Variables.QUESTION_STATION, context=text)['answer']
        result = get_station_name(answer.strip(), Variables.STATIONS)
        return result[0]

    def extract_date(self, text) -> str:
        #tokens = nltk.word_tokenize(text)
        # time_delta = timedelta(days=18)
        text = translate_date(words_to_numbers(change_weird_words_to_normal(split_hyphenated_words(text))))

        for k, v in Variables.HALF.items():
            text = text.replace(k, str(v))
        text = lemmatize_sentence(text)
        if 'следующий' in text:
            text = text.replace('следующий', 'через 1')
        if 'прошлый' in text:
            text = text.replace('прошлый', '1')
        if 'позавчера' in text:
            text = text.replace('позавчера', '2 дня назад')
        if 'вчера' in text:
            text = text.replace('вчера', '1 день назад')
        if 'неделю назад' in text:
            text = text.replace('неделю назад', '1 неделю назад')

        matches = re.findall(Variables.PATTERN, text)
        try:
            res = str(dateparser.parse(matches[0], settings={'DATE_ORDER': 'YMD'})).split(' ')[0]
            if res != 'None':
                res2 = datetime.datetime.strptime(res, '%Y-%m-%d')
                # res2 -= time_delta TODO
                return res2.strftime("%Y-%m-%d")
        except IndexError:
            pass
        answer = model_pipeline(question=Variables.QUESTION_DATE, context=text)['answer']
        answer = translate_date(words_to_numbers(change_weird_words_to_normal(split_hyphenated_words(answer))))
        res = str(dateparser.parse(answer, settings={'DATE_ORDER': 'YMD'})).split(' ')[0]
        if res != 'None':
                check_day = check_weekday_in_text(text)
                if check_day:
                    res = change_day_of_week(res, check_day[1])
                    res2 = datetime.datetime.strptime(res, '%Y-%m-%d')
                    # res2 -= time_delta TODO
                    return res2.strftime("%Y-%m-%d")
                else:
                    res2 = datetime.datetime.strptime(res, '%Y-%m-%d')
                    # res2 -= time_delta TODO
                    return res2.strftime("%Y-%m-%d")
        return 'Incorrect request'


if __name__ == '__main__':
    print('Извлечение даты и времени из текста')
    text = 'Скажи данные о пассажиропотоке вчера на станции метро Сокольник'
    extractor = MetroDataExtractor()
    print(extractor.extract_station(text), extractor.extract_date(text))
