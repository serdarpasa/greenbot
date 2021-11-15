from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext


async def get_help(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    button_write = types.InlineKeyboardButton('Написать', callback_data='help_w')
    button_site = types.InlineKeyboardButton('Помощь на сайте', url='https://greenwayminsk.by/faq')
    button_call = types.InlineKeyboardButton('Позвонить', callback_data='help_c')
    markup.row(button_write)
    markup.row(button_site)
    markup.row(button_call)
    await message.answer('Выберите вариант', reply_markup=markup)


async def help_actions(call: types.CallbackQuery):
    if call.data == 'help_w':
        await call.message.answer('Напишите сообщение')
    elif call.data == 'help_c':
        await call.message.answer('Позвоните на горячую линию: тел +375291234567')
    await call.message.answer('hellllp')


async def news(message: types.Message):
    await message.answer('Новости: https://beegreen.by/')

def register_help(dp: Dispatcher):
    dp.register_message_handler(get_help, commands=['help'])
    dp.register_message_handler(help_actions, lambda call: call.data.startswith('help'))
    dp.register_message_handler(news, commands=['news'])