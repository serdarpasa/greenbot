import asyncio

import sys
import os

import importlib

import typing

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.expanduser(BASE_DIR)
if path not in sys.path:
    sys.path.insert(0, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenway.settings")
django.setup()



TOKEN = '2124163604:AAG36f9I074pcWDl3h9aSd2b4Yr06te2r2k'
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

delivery_cb = CallbackData('delivery', 'id', 'address', 'action')

POSTS = {
    str(index): {
        'title': f'Post {index}',
        'body': 'Lorem ipsum dolor sit amet, ',
        'votes': index*2,
    } for index in range(1, 6)
}

posts_cb = CallbackData('post_le', 'id', 'body', 'action')  # post:<id>:<action>


async def set_commands(dp=dp):  # dp=dp only for arg placeholder: func gets and dp inst
    commands = [
        types.BotCommand(command='/order', description='Индивидуальный заказ'),
        types.BotCommand(command='/group_order', description='Груповой заказ'),
        types.BotCommand(command='/help', description='Помощь'),
        types.BotCommand(command='/news', description='Новости')
    ]
    await dp.bot.set_my_commands(commands)
    print('commands are loaded')


@dp.message_handler(commands=['help'])
async def helf(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    button_write = types.InlineKeyboardButton('Написать', callback_data='help_w')
    button_site = types.InlineKeyboardButton('Помощь на сайте', url='https://greenwayminsk.by/faq')
    button_call = types.InlineKeyboardButton('Позвонить', callback_data='help_c')
    markup.row(button_write)
    markup.row(button_site)
    markup.row(button_call)
    await message.answer('Выберите вариант', reply_markup=markup)


# @dp.callback_query_handler(lambda data: data.message.text.startswith('help_'))
@dp.callback_query_handler(lambda call: call.data.startswith('help'))
async def help_actions(call: types.CallbackQuery):
    if call.data == 'help_w':
        await call.message.answer('Напишите сообщение')
    elif call.data == 'help_c':
        await call.message.answer('Позвоните на горячую линию: тел +375291234567')
    await call.message.answer('hellllp')


@dp.message_handler(commands=['/order'])



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Hello world')
    markup = types.InlineKeyboardMarkup()
    for post_id, post in POSTS.items():
        markup.add(
            types.InlineKeyboardButton(
                post['title'],
                callback_data=posts_cb.new(id=post_id, body='ololo', action='view')),
        )
    await message.reply('psts', reply_markup=markup)


@dp.callback_query_handler(posts_cb.filter(action='view'))
async def query_view(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    post_id = callback_data['id']
    print('view')
    post = POSTS.get(post_id, None)
    if not post:
        return await query.answer('Unknown post!')


class Order(StatesGroup):
    number = State()
    surname = State()
    phone = State()
    choose_comment = State()
    comment = State()
    choose_delivery = State()
    address = State()
    confirm = State()


@dp.message_handler(commands=['order'])
async def start_order(message: types.Message):
    await message.reply(f'Введите номер заказа', reply_markup=types.ReplyKeyboardRemove())
    await Order.number.set()


@dp.message_handler(state=Order.number)
async def order_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)

    await message.reply('Введите Фамилию (заказчика)')
    await Order.next()


@dp.message_handler(state=Order.surname)
async def order_name(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)

    await message.reply('Введите Ваш номер мобильного телефона')
    await Order.next()


@dp.message_handler(state=Order.phone)
async def order_name(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)

    keyboard = types.ReplyKeyboardMarkup()
    button_yes = types.KeyboardButton('Оставить комментарий')
    button_no = types.KeyboardButton('Продолжить')
    keyboard.add(button_yes, button_no)
    await message.answer("Хотите оставить коментарий?", reply_markup=keyboard)
    await Order.next()


@dp.message_handler(lambda message: message.text in ['Оставить комментарий', 'Продолжить'],
                    state=Order.choose_comment)
async def order_choose_comment(message: types.Message, state: FSMContext):
    if message.text == 'Оставить комментарий':
        await message.answer('Введите свой комментайрий:', reply_markup=types.ReplyKeyboardRemove())
        await Order.next()
    else:
        keyboard = types.ReplyKeyboardMarkup()
        button_outlet = types.KeyboardButton('До пункта выдачи')
        button_door = types.KeyboardButton('До двери')
        keyboard.add(button_outlet, button_door)
        await message.answer("Выберите тип доставки", reply_markup=keyboard)
        await Order.choose_delivery.set()


@dp.message_handler(state=Order.comment)
async def order_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)

    keyboard = types.ReplyKeyboardMarkup()
    button_outlet = types.KeyboardButton('До пункта выдачи')
    button_door = types.KeyboardButton('До двери')
    keyboard.add(button_outlet, button_door)
    await message.answer("Выберите тип доставки", reply_markup=keyboard)
    await Order.next()


@dp.message_handler(lambda message: message.text in ['До пункта выдачи', 'До двери'],
                    state=Order.choose_delivery)
async def order_choose_delivery(message: types.Message, state: FSMContext):
    if message.text == 'До пункта выдачи':
        print('пункт выдачи')
        keyboard = types.ReplyKeyboardMarkup()
        for location_id, location in location_test.items():
            keyboard.add(
                types.KeyboardButton(text=location['title'])
            )
        await message.answer('Выберите пункт выдачи используя клавиатуру ниже', reply_markup=keyboard)
        await state.update_data(choose_delivery='outlet')
        await Order.next()

    else:
        await message.answer('Введите адрес для доставки', reply_markup=types.ReplyKeyboardRemove())
        await state.update_data(choose_delivery='to_door')
        await Order.next()


@dp.message_handler(state=Order.address)
async def order_delivery_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    user_data = await state.get_data()
    await message.answer('Подтвердите введенную информацию:')

    keyboard = types.ReplyKeyboardMarkup()
    button_yes = types.KeyboardButton('Да, информация верна')
    button_no = types.KeyboardButton('Нет, начать заного')
    keyboard.add(button_yes, button_no)
    await bot.send_message(message.chat.id, user_data, reply_markup=keyboard)
    await Order.next()


@dp.message_handler(lambda message: message.text in ['Да, информация верна', 'Нет, начать заного'],
                    state=Order.confirm)
async def order_confirm(message: types.Message, state: FSMContext):
    if message.text == 'Да, информация верна':
        await message.answer('Заказ подтвержден, менерджер с вами свяжется', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Нет, начать заного':
        await message.answer('Начните заного', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('Пожлуйста, используйте клавиатуру для ответа')
    await state.finish()


@dp.message_handler(state=[Order.confirm, Order.choose_delivery, Order.choose_comment])
async def order_error(message: types.Message, state: FSMContext):
    return await message.reply('Пожалуйста, используйте клавиатуру')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_commands)
