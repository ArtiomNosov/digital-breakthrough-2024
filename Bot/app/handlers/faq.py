from aiogram import Dispatcher, types
async def faq_start(message: types.Message):
    answer_message = '''
/start - перезапуск диалога
/agg_period - получение статистики за диапазон дат
    '''
    await message.answer(answer_message)

def register_handlers_faq(dp: Dispatcher):
    dp.register_message_handler(faq_start, commands='faq', state='*')

