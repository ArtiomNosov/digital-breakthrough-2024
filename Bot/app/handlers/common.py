from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from Model_1.model_1 import *
from model.model import MetroDataExtractor

from app.db.functions import get_passenger_flow_from_db
from app.db.functions import get_agg_passenger_flow_from_db
from app.db.functions import save_message_to_db


class Diologue(StatesGroup):
    waiting_for_question = State()
    answer_for_question = State()
    waiting_for_question_model_2 = State()
    agg_period = State()
    agg_period_2 = State()
    agg_period_3 = State()
    agg_period_4 = State()


async def cmd_start(message: types.Message, state: FSMContext):
    msg_bot = '''Привет, я могу помочь найти курс, чтобы попасть на работу мечты!

Можешь просто отправить ссылку вакансии, а в ответ пришлём тебе наиболее подходящие для неё курсы!
'''
    await message.answer(msg_bot, reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(msg_bot=msg_bot)
    await state.set_state(Diologue.waiting_for_question.state)


# async def cmd_cancel(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove())

# Просто функция, которая доступна только администратору,
# чей ID указан в файле конфигурации.

import datetime
import json

answer_prompt = '''
Сегодня: {}
Дата просмотра: {}
На сколько дней сдвиг: {}
Cтанция: {}
Пассажиропоток: {}
'''
# TODO Линия: {}

stations = ["Яхромская", "Ясенево", "Южная", "Юго-Западная", "Юго-Восточная",
            "Электрозаводская", "Щукинская", "Щёлковская", "Шоссе Энтузиастов", "Шипиловская", "Шелепиха",
            "Шаболовская", "Чкаловская", "Чистые пруды",
            "Чеховская", "Чертановская", "Черкизовская", "ЦСКА", "Цветной Бульвар", "Царицыно", "Хорошёвская",
            "Хорошевская", "Хорошёво", "Ховрино",
            "Фрунзенская", "Фонвизинская", "Фили", "Филёвский парк", "Филатов луг", "Физтех", "Университет",
            "Улица Скобелевская", "Улица Дмитриевского",
            "Улица Горчакова", "Улица Академика Янгеля", "Улица 1905 года", "Угрешская", "Тушинская", "Тургеневская",
            "Тульская", "Трубная",
            "Тропарёво", "Третьяковская", "ТПУ Рязанская", "Тимирязевская", "Технопарк", "Терехово", "Тёплый стан",
            "Текстильщики", "Театральная",
            "Тверская", "Таганская", "Сходненская", "Сухаревская", "Студенческая", "Строгино", "Стрешнево", "Стенд",
            "Станционная", "Старокачаловская",
            "Сретенский Бульвар", "Спортивная", "Спартак", "Солнцево", "Сокольники", "Соколиная Гора", "Сокол",
            "Смоленская", "Славянский бульвар",
            "Серпуховская", "Семёновская", "Селигерская", "Севастопольская", "Свиблово", "Саларьево", "Савёловская",
            "Рязанский Проспект",
            "Румянцево", "Ростокино", "Римская", "Рижская", "Речной вокзал", "Рассказовка", "Раменки",
            "Пятницкое шоссе", "Пыхтино", "Пушкинская",
            "Профсоюзная", "Проспект Мира", "Проспект Вернадского", "Пролетарская", "Прокшино",
            "Преображенская площадь", "Пражская", "Полянка",
            "Полежаевская", "Площадь Революции", "Площадь Ильича", "Площадь Гагарина", "Планерная", "Пионерская",
            "Печатники", "Петровско-Разумовская",
            "Петровский парк", "Перово", "Первомайская", "Партизанская", "Парк Победы", "Парк культуры", "Панфиловская",
            "Павелецкая", "Охотный ряд", "Отрадное",
            "Орехово", "Ольховая", "Октябрьское поле", "Октябрьская", "Окская", "Окружная", "Озёрная",
            "Новые Черёмушки", "Новоясеневская", "Новохохловская",
            "Новослободская", "Новопеределкино", "Новокузнецкая", "Новокосино", "Новогиреево", "Новаторская",
            "Нижегородская", "Некрасовка",
            "Нахимовский Проспект", "Народное Ополчение", "Нагорная", "Нагатинский затон", "Нагатинская", "Мякинино",
            "Москва-Сити", "Молодёжная", "Мнёвники",
            "Мичуринский проспект", "Митино", "Минская", "Менделеевская", "Медведково", "Маяковская", "Марьино",
            "Марьина Роща", "Марксистская", "Люблино",
            "Лухмановская", "Лужники", "Лубянка", "Ломоносовский проспект", "Ломоносовский проспект", "Локомотив",
            "Лихоборы", "Лианозово", "Лефортово",
            "Лесопарковая", "Лермонтовский проспект", "Ленинский Проспект", "Кутузовская", "Курская", "Кунцевская",
            "Кузьминки", "Кузнецкий мост",
            "Крымская", "Крылатское", "Кропоткинская", "Крестьянская застава", "Красные ворота", "Красносельская",
            "Краснопресненская", "Красногвардейская",
            "Котельники", "Косино", "Коптево", "Коньково", "Комсомольская", "Коммунарка", "Коломенская", "Кожуховская",
            "Кленовый бульвар", "Китай-город", "Киевская",
            "Каширская", "Каховская", "Кантемировская", "Калужская", "Измайловская", "Измайлово", "Зябликово", "Зюзино",
            "Зорге", "ЗИЛ", "Жулебино", "Дубровка",
            "Достоевская", "Домодедовская", "Добрынинская", "Дмитровская", "Динамо", "Деловой центр", "Давыдково",
            "Говорово", "Выхино", "Воронцовская",
            "Воробьёвы горы", "Волоколамская", "Волжская", "Волгоградский проспект", "Войковская", "Водный Стадион",
            "Владыкино", "Верхние Лихоборы",
            "Верхние Котлы", "ВДНХ", "Варшавская", "Бутырская", "Бунинская аллея", "Бульвар Рокоссовского",
            "Бульвар Дмитрия Донского", "Бульвар Адмирала Ушакова",
            "Братиславская", "Ботанический сад", "Боровское шоссе", "Боровицкая", "Борисово", "Битцевский парк",
            "Библиотека имени Ленина", "Бибирево",
            "Беляево", "Белорусская", "Беломорская", "Белокаменная", "Беговая", "Бауманская", "Баррикадная",
            "Балтийская", "Багратионовская", "Бабушкинская",
            "Аэропорт Внуково", "Аэропорт", "Арбатская", "Аннино", "Андроновка", "Аминьевская", "Алтуфьево",
            "Алма-Атинская", "Алексеевская",
            "Александровский сад", "Академическая",
            "Административная", "Автозаводская", "Авиамоторная"]

get_station_fromat = '''
Твоя задача получить из текстововго запроса название станции метро в формате <название станции метро>
Если что то не удалось найти в запросе, то пиши None. Если метро указано с ошибкой, то получи наиболее похожее название.
Примеры:
1. "Сокол" -> <Сокол>
Запрос: "{}"
'''
# Полный список станций: {}


async def get_station(question):
    full_prompt = get_station_fromat.format(question, ', '.join(stations))
    answer = get_chat_completion(giga_token, full_prompt)
    station = answer.json()['choices'][0]['message']['content']
    station = station.replace('Ответ: ', '')
    station = station.replace('.', '')
    station = station.replace('<', '')
    station = station.replace('>', '')
    station = station.replace('"', '')
    station = station.replace('"', '')
    print(f'get_station = {station}')
    if station not in stations:
        raise Exception('Станция не определена')
        return
    return station


get_date_prompt = '''
Твоя задача получить из текстововго запроса дату в формате год-месяц-день.
Если что то не удалось найти в запросе, то пиши None. Если указано сегодня, завтра или неделю назад, то считай относительно текущей даты.
Сегодняшняя дата: {}
Запрос: {}
'''


async def get_date(question, today):
    full_prompt = get_date_prompt.format(today, question)
    answer = get_chat_completion(giga_token, full_prompt)
    date = answer.json()['choices'][0]['message']['content']
    date = date.replace('Ответ: ', '')
    date = date.replace('.', '')
    print(f'get_date = {date}')
    return date


get_date_gap_prompt = '''
Твоя задача получить из текстововго запроса на сколько дней идёт сдвиг относительно текущего врмени в днях.
Если речь идёт о будущем, то число положительное
Если речь идёт о прошлом, то число отрицательное
Если что то не удалось найти в запросе, то пиши None. Если указано сегодня, завтра или неделю назад, то считай относительно текущей даты.
Сегодняшняя дата: {}
Сегодняшний день недели: {}
Запрос: {}
'''
async def get_date_gap(question, today):
    today_date = datetime.datetime.fromisoformat(today)
    weekday = today_date.weekday()
    full_prompt = get_date_gap_prompt.format(today, weekday, question)
    answer = get_chat_completion(giga_token, full_prompt)
    text_answer_day = answer.json()['choices'][0]['message']['content']
    text_answer_day = text_answer_day.replace('.', '')
    text_answer_day = text_answer_day.replace('"', '')
    print(f'text_answer_day: {text_answer_day}')
    print(f'get_date_gap = {text_answer_day}')
    return text_answer_day

async def get_date_res_date(question, today):
    date_today = datetime.datetime.fromisoformat(today)
    text_day = await get_date(question, today)
    text_day_gap = await get_date_gap(question, today)

    try:
        int_day = int(text_day_gap.split()[-1])
    except Exception:
        int_day = None

    res_text_date = None
    if 'None' in text_day and int_day is None:
        raise Exception('Не распознана дата')
    elif 'None' not in text_day:
        res_text_date = text_day
    elif int_day is not None:
        dt_full = date_today + datetime.timedelta(days=int_day)
        res_text_date = str(dt_full)[0:10]
    res_text_date.replace('.', '')
    res_text_date = res_text_date.split()[-1]
    try:
        final_int_day = datetime.datetime.fromisoformat(res_text_date) - date_today
    except Exception as e:
        res_text_date = today
        final_int_day = datetime.datetime.fromisoformat(res_text_date) - date_today
        print(f'get_date_res_date e={e}')
    final_int_day = final_int_day.days
    print(f'res_text_date: {res_text_date}, final_int_day: {final_int_day}')
    return res_text_date, final_int_day

get_agg_prompt = '''
Твоя задача получить из текстововго запроса какую из агрегирующих функий [SUM, AVG, MIN, MAX, COUNT] нужно применить.
Если что то не удалось найти в запросе, то пиши None.
Запрос: {}
'''
async def get_from_list(text, list_arr):
    for val in list_arr:
        if val in text:
            return val

    return None
async def get_agg(question):
    full_prompt = get_agg_prompt.format(question)
    answer = get_chat_completion(giga_token, full_prompt)
    text_answer = answer.json()['choices'][0]['message']['content']
    print(f'get_agg: {text_answer}')
    result = await get_from_list(text_answer, ['SUM', 'AVG', 'MIN', 'MAX', 'COUNT'])
    return result

async def get_str_passenger_flow(passenger_flow):
    str_passenger_flow = '\n'
    if passenger_flow:
        for val1, val2 in passenger_flow:
            val1 = str(val1).lower().capitalize()
            str_passenger_flow += f'  * На линии "{val1}" пассажиропоток равен {int(val2)}\n'
    if str_passenger_flow == '\n':
        str_passenger_flow += '  * На эту дату информации нет'
    return str_passenger_flow

async def answer_question(message: types.Message, state: FSMContext):
    question = message.text

    # сохраняем сообщение
    user_data = await state.get_data()
    msg_bot = user_data.get('msg_bot')
    await save_message_to_db(message.from_id, msg_bot, question)

    print(f'Test мы получили сообщение переходим в состояние answer_for_question: {question}')
    await message.answer('Запрос обрабатывается...')

    try:
        station = await get_station(question)
        # запрос SQL
        today = '2024-04-03'
        res_text_date, final_int_day = await get_date_res_date(question, today)
        line_name = None  # TODO убрать

        passenger_flow = await get_passenger_flow_from_db(station, line_name, res_text_date)  # res_dict
        str_passenger_flow = await get_str_passenger_flow(passenger_flow)
        # line_name,
        answer_msg_bot = answer_prompt.format(today, res_text_date, final_int_day, station, str(str_passenger_flow))
        await message.answer(answer_msg_bot)

        # сохраняем сообщение
        await save_message_to_db(message.from_id, answer_msg_bot, question)

    except Exception as e:
        print(e)
        answer_msg_bot = f'Проверьте корректность вашего запроса. Ошибка: {e}'
        await save_message_to_db(message.from_id, answer_msg_bot, question)
        await message.answer(answer_msg_bot)
    await state.set_state(Diologue.waiting_for_question.state)

async def get_station_model_2(question):
    m2 = MetroDataExtractor()
    return m2.extract_station(question)

async def get_date_model_2(question):
    m2 = MetroDataExtractor()
    return m2.extract_date(question)

async def hello_answer_question_model_2(message: types.Message, state: FSMContext):
    msg_bot = 'Был осуществлён переход на нашу модель'
    await message.answer(msg_bot)
    await state.update_data(msg_bot=msg_bot)
    await state.set_state(Diologue.waiting_for_question_model_2.state)

async def answer_question_model_2(message: types.Message, state: FSMContext):
    question = message.text

    # сохраняем сообщение
    user_data = await state.get_data()
    msg_bot = user_data.get('msg_bot')
    await save_message_to_db(message.from_id, msg_bot, question)

    await message.answer('Запрос обрабатывается нашей моделью...')
    today = '2024-04-03'
    try:
        station = await get_station_model_2(question)
        # запрос SQL
        res_text_date = await get_date_model_2(question)
        if station == 'I':
            raise Exception('Не распознано метро')
        if res_text_date == 'Incorrect request':
            raise Exception('Не распознана дата')
        print('model_2')
        print(f'station: {station}')
        print(f'res_text_date: {res_text_date}')

        passenger_flow = await get_passenger_flow_from_db(station, None, res_text_date)  # res_dict
        str_passenger_flow = await get_str_passenger_flow(passenger_flow)
        date_today = datetime.datetime.fromisoformat(today)
        final_int_day = datetime.datetime.fromisoformat(res_text_date) - date_today
        final_int_day = final_int_day.days
        answer_msg_bot = answer_prompt.format(today, res_text_date, final_int_day, station, str(str_passenger_flow))
        await message.answer(answer_msg_bot)
        # сохраняем сообщение
        await save_message_to_db(message.from_id, answer_msg_bot, question)
    except Exception as e:
        answer_msg_bot = f'Проверьте корректность вашего запроса. Ошибка: {e}'
        await save_message_to_db(message.from_id, answer_msg_bot, question)
        print(e)
        await message.answer()
    await state.set_state(Diologue.waiting_for_question_model_2.state)


async def secret_command(message: types.Message):
    await message.answer("Поздравляю! Эта команда доступна только администратору бота.")

async def agg_period_command(message: types.Message, state: FSMContext):
    msg_bot = 'Введи дату начала диапазона'
    await message.answer(msg_bot)
    await state.update_data(msg_bot=msg_bot)
    await state.set_state(Diologue.agg_period.state)
async def get_agg_period(message: types.Message, state: FSMContext):
    question = message.text

    # сохраняем сообщение
    user_data = await state.get_data()
    msg_bot = user_data.get('msg_bot')
    await save_message_to_db(message.from_id, msg_bot, question)

    today = '2024-04-03'
    try:
        print(f'question: {message.text}')
        res_text_date1, final_int_day1 = await get_date_res_date(question, today)
        msg_bot = 'Введи дату конца диапазона'
        await message.answer(msg_bot)
        await state.update_data(question_1=question)
        await state.update_data(msg_bot=msg_bot)
        await state.update_data(d_res_text_date1=res_text_date1)
        await state.update_data(d_final_int_day1=final_int_day1)
        await state.set_state(Diologue.agg_period_2.state)
    except Exception as e:
        print(e)
        await message.answer('Проверьте корректность вашего запроса. Перезапустите /agg_period')
        await state.set_state(Diologue.waiting_for_question.state)

async def get_agg_period_2(message: types.Message, state: FSMContext):
    question = message.text

    # сохраняем сообщение
    user_data = await state.get_data()
    msg_bot = user_data.get('msg_bot')
    await save_message_to_db(message.from_id, msg_bot, question)

    today = '2024-04-03'
    try:
        # user_data = await state.get_data()
        # user_data.get('photo')
        res_text_date2, final_int_day2 = await get_date_res_date(question, today)
        await state.update_data(question_2=question)
        await state.update_data(d_res_text_date2=res_text_date2)
        await state.update_data(d_final_int_day2=final_int_day2)
        msg_bot = 'Введите станцию метро'
        await message.answer(msg_bot)
        await state.update_data(msg_bot=msg_bot)
        await state.set_state(Diologue.agg_period_3.state)
    except:
        await message.answer('Проверьте корректность вашего запроса. Перезапустите /agg_period')
        await state.set_state(Diologue.waiting_for_question.state)

async def get_agg_period_3(message: types.Message, state: FSMContext):
    question = message.text

    # сохраняем сообщение
    user_data = await state.get_data()
    msg_bot = user_data.get('msg_bot')
    await save_message_to_db(message.from_id, msg_bot, question)

    try:
        station = await get_station(question)
        await state.update_data(question_3=question)
        await state.update_data(d_station=station)
        msg_bot = 'Введите агрегирующую функцию'
        await message.answer(msg_bot)
        await state.update_data(msg_bot=msg_bot)
        await state.set_state(Diologue.agg_period_4.state)
    except:
        await message.answer('Проверьте корректность вашего запроса. Перезапустите /agg_period')
        await state.set_state(Diologue.waiting_for_question.state)

async def get_agg_period_4(message: types.Message, state: FSMContext):
    question = message.text
    user_data = await state.get_data()
    question_1 = user_data.get('question_1')
    question_2 = user_data.get('question_2')
    question_3 = user_data.get('question_3')
    all_q = '{'+'"question_1": "{}", "question_2": "{}", "question_3": "{}", "question_4": "{}"'.format(question_1, question_2, question_3, question)+'}'
    # сохраняем сообщение
    msg_bot = user_data.get('msg_bot')
    await save_message_to_db(message.from_id, msg_bot, question)

    today = '2024-04-03'
    try:
        agg = await get_agg(question) # 'AVG'
        # await state.update_data(question_4=question)
        user_data = await state.get_data()
        station = user_data.get('d_station')
        print(f'get_agg_period_4 station: {station}')
        res_text_date1 = user_data.get('d_res_text_date1')
        print(f'res_text_date1: {res_text_date1}')
        res_text_date2 = user_data.get('d_res_text_date2')
        print(f'res_text_date2: {res_text_date2}')
        agg_passenger_flow = await get_agg_passenger_flow_from_db(agg, station, res_text_date1, res_text_date2)
        str_agg_passenger_flow = await get_str_passenger_flow(agg_passenger_flow)
        answer_msg_bot = f'''
Сегодня: {today}
Дата просмотра: c {res_text_date1} по {res_text_date2}
Метрика: {agg}
Cтанция: {station}
Пассажиропоток: {str_agg_passenger_flow}
            '''
        await message.answer(answer_msg_bot)
        # сохраняем сообщение
        await save_message_to_db(message.from_id, answer_msg_bot, all_q)

        await state.set_state(Diologue.waiting_for_question.state)
    except Exception as e:
        print(e)
        answer_msg_bot = 'Проверьте корректность вашего запроса. Перезапустите /agg_period'
        await save_message_to_db(message.from_id, answer_msg_bot, all_q)
        await message.answer(answer_msg_bot)
        await state.set_state(Diologue.waiting_for_question.state)

import re
def register_hendlers_common(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_message_handler(answer_question, regexp=re.compile(r"^[^/].*"), state=Diologue.waiting_for_question)
    dp.register_message_handler(hello_answer_question_model_2, commands='start_our_model', state='*')
    dp.register_message_handler(answer_question_model_2, regexp=re.compile(r"^[^/].*"), state=Diologue.waiting_for_question_model_2)
    # dp.register_message_handler(model_answer, state=Diologue.answer_for_question)
    # dp.register_message_handler(cmd_cancel, commands='cancel', state='*')
    # dp.register_message_handler(cmd_cancel, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(secret_command, IDFilter(user_id=admin_id), commands='abracadabra')
    dp.register_message_handler(agg_period_command, commands='agg_period', state='*')
    dp.register_message_handler(get_agg_period, state=Diologue.agg_period)
    dp.register_message_handler(get_agg_period_2, state=Diologue.agg_period_2)
    dp.register_message_handler(get_agg_period_3, state=Diologue.agg_period_3)
    dp.register_message_handler(get_agg_period_4, state=Diologue.agg_period_4)
