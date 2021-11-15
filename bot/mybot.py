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

from bot.handlers.individual_order import register_individual_order
from bot.handlers.help import register_help


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


if __name__ == '__main__':
    register_individual_order(dp)
    register_help(dp)
    executor.start_polling(dp, on_startup=set_commands)
