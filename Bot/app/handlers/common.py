from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from ModelGigaChad.model import *
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

import datetime
import json

async def answer_question(message: types.Message, state: FSMContext):
    question = message.text
    msg_bot = 'Идёт обработка ссылки...'
    await message.answer(msg_bot)
    # await state.update_data(msg_bot=msg_bot)
    msg_bot_answer
    await save_message_to_db(message.from_id, msg_bot, question)

    await state.set_state(Diologue.waiting_for_question_model_2.state)

async def answer_question_model_2(message: types.Message, state: FSMContext):
    question = message.text

    # сохраняем сообщение
    user_data = await state.get_data()
    msg_bot = user_data.get('msg_bot')
    await save_message_to_db(message.from_id, msg_bot, question)
#
#     await message.answer('Запрос обрабатывается нашей моделью...')
#     today = '2024-04-03'
#     try:
#         station = await get_station_model_2(question)
#         # запрос SQL
#         res_text_date = await get_date_model_2(question)
#         if station == 'I':
#             raise Exception('Не распознано метро')
#         if res_text_date == 'Incorrect request':
#             raise Exception('Не распознана дата')
#         print('model_2')
#         print(f'station: {station}')
#         print(f'res_text_date: {res_text_date}')
#
#         passenger_flow = await get_passenger_flow_from_db(station, None, res_text_date)  # res_dict
#         str_passenger_flow = await get_str_passenger_flow(passenger_flow)
#         date_today = datetime.datetime.fromisoformat(today)
#         final_int_day = datetime.datetime.fromisoformat(res_text_date) - date_today
#         final_int_day = final_int_day.days
#         answer_msg_bot = answer_prompt.format(today, res_text_date, final_int_day, station, str(str_passenger_flow))
#         await message.answer(answer_msg_bot)
#         # сохраняем сообщение
#         await save_message_to_db(message.from_id, answer_msg_bot, question)
#     except Exception as e:
#         answer_msg_bot = f'Проверьте корректность вашего запроса. Ошибка: {e}'
#         await save_message_to_db(message.from_id, answer_msg_bot, question)
#         print(e)
#         await message.answer()
#     await state.set_state(Diologue.waiting_for_question_model_2.state)


async def secret_command(message: types.Message):
    await message.answer("Поздравляю! Эта команда доступна только администратору бота.")

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
    # dp.register_message_handler(agg_period_command, commands='agg_period', state='*')
    # dp.register_message_handler(get_agg_period, state=Diologue.agg_period)
    # dp.register_message_handler(get_agg_period_2, state=Diologue.agg_period_2)
    # dp.register_message_handler(get_agg_period_3, state=Diologue.agg_period_3)
    # dp.register_message_handler(get_agg_period_4, state=Diologue.agg_period_4)
