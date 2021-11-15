import typing

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData


TOKEN = '2124163604:AAG36f9I074pcWDl3h9aSd2b4Yr06te2r2k'
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

delivery_cb = CallbackData('delivery', 'id', 'address', 'action')

location_test = {
    str(index): {
        'title': f'loca {index}',
        'address': 'Lorem ipsum',
    } for index in range(1, 5)
}

POSTS = {
    str(index): {
        'title': f'Post {index}',
        'body': 'Lorem ipsum dolor sit amet, ',
        'votes': index*2,
    } for index in range(1, 6)
}

posts_cb = CallbackData('post_le', 'id', 'body', 'action')  # post:<id>:<action>


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
    print(f'post items: {post_id} {post}')
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


@dp.message_handler(commands=['order'])
async def start_order(message: types.Message):
    await message.reply(f'Введите номер заказа')
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


@dp.message_handler(state=Order.choose_comment)
async def order_choose_comment(message: types.Message, state: FSMContext):
    if message.text == 'Оставить комментарий':
        await message.answer('Введите свой комментайрий:')
        await Order.next()
    elif message.text == 'Продолжить':
        keyboard = types.ReplyKeyboardMarkup()
        button_outlet = types.KeyboardButton('До пункта выдачи')
        button_door = types.KeyboardButton('До двери')
        keyboard.add(button_outlet, button_door)
        await message.answer("Выберите тип доставки", reply_markup=keyboard)
        await Order.choose_delivery.set()
    else:
        pass


@dp.message_handler(state=Order.comment)
async def order_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)

    keyboard = types.ReplyKeyboardMarkup()
    button_outlet = types.KeyboardButton('До пункта выдачи')
    button_door = types.KeyboardButton('До двери')
    keyboard.add(button_outlet, button_door)
    await message.answer("Выберите тип доставки", reply_markup=keyboard)
    await Order.next()


@dp.message_handler(state=Order.choose_delivery)
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

    elif message.text == 'До двери':
        await message.answer('Введите адрес для доставки')
        await state.update_data(choose_delivery='to_door')
        await Order.next()
    else:
        print('%((((')


@dp.message_handler(state=Order.address)
async def order_delivery_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer(f'Доставка будет по аддресу: {message.text}')
    user_data = await state.get_data()
    await message.answer(f"{user_data['address']}, {user_data['choose_delivery']}, {user_data}")
    await state.finish()


executor.start_polling(dp)