from aiogram import Dispatcher, types

async def support_start(message: types.Message):
    answer_message = '''
Попробуйте перезапустить бота командой /start

С техническими вопросами обращаться @Artiom_Nosov
    '''
    await message.answer(answer_message)

def register_handlers_support(dp: Dispatcher):
    dp.register_message_handler(support_start, commands='support', state='*')