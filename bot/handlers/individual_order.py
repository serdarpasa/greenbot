import sys
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from asgiref.sync import sync_to_async

import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.expanduser(BASE_DIR)
if path not in sys.path:
    sys.path.insert(0, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenway.settings")
django.setup()

from bot.models import PersonalOrder, TelegramUser

location_test = {
    str(index): {
        'title': f'loca {index}',
        'address': 'Lorem ipsum',
    } for index in range(1, 5)
}


class Order(StatesGroup):
    number = State()
    surname = State()
    phone = State()
    choose_comment = State()
    comment = State()
    choose_delivery = State()
    address = State()
    confirm = State()


async def start_order(message: types.Message):
    await message.reply(f'Введите номер заказа', reply_markup=types.ReplyKeyboardRemove())
    await Order.number.set()


async def order_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)

    await message.reply('Введите Фамилию (заказчика)')
    await Order.next()


async def order_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)

    await message.reply('Введите Ваш номер мобильного телефона')
    await Order.next()


async def order_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)

    keyboard = types.ReplyKeyboardMarkup()
    button_yes = types.KeyboardButton('Оставить комментарий')
    button_no = types.KeyboardButton('Продолжить')
    keyboard.add(button_yes, button_no)
    await message.answer("Хотите оставить коментарий?", reply_markup=keyboard)
    await Order.next()


async def order_choose_comment(message: types.Message, state: FSMContext):
    if message.text == 'Оставить комментарий':
        await message.answer('Введите свой комментайрий:', reply_markup=types.ReplyKeyboardRemove())
        await Order.next()
    else:
        keyboard = types.ReplyKeyboardMarkup()
        button_outlet = types.KeyboardButton('До пункта выдачи')
        button_door = types.KeyboardButton('До двери')
        keyboard.add(button_outlet, button_door)
        await state.update_data(comment=None)
        await message.answer("Выберите тип доставки", reply_markup=keyboard)
        await Order.choose_delivery.set()


async def order_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)

    keyboard = types.ReplyKeyboardMarkup()
    button_outlet = types.KeyboardButton('До пункта выдачи')
    button_door = types.KeyboardButton('До двери')
    keyboard.add(button_outlet, button_door)
    await message.answer("Выберите тип доставки", reply_markup=keyboard)
    await Order.next()


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


async def order_delivery_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    user_data = await state.get_data()
    await message.answer('Подтвердите введенную информацию:')

    keyboard = types.ReplyKeyboardMarkup()
    button_yes = types.KeyboardButton('Да, информация верна')
    button_no = types.KeyboardButton('Нет, начать заного')
    keyboard.add(button_yes, button_no)
    # await bot.send_message(message.chat.id, user_data, reply_markup=keyboard)
    await message.answer(user_data, reply_markup=keyboard)
    await Order.next()


async def order_confirm(message: types.Message, state: FSMContext):
    if message.text == 'Да, информация верна':
        user_data = await state.get_data()
        await create_order(user_data)

        await message.answer('Заказ подтвержден, менерджер с вами свяжется', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Нет, начать заного':
        await message.answer('Начните заного', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('Пожлуйста, используйте клавиатуру для ответа')
    await state.finish()


async def order_error(message: types.Message, state: FSMContext):
    return await message.reply('Пожалуйста, используйте клавиатуру')


@sync_to_async
def create_order(user_data):
    new_order = PersonalOrder.objects.create(
        code=user_data['number'],
        tel_number=user_data['phone'],
        surname=user_data['surname'],
        comment=user_data['comment'],
        delivery_type=user_data['choose_delivery'],
        delivery_address=user_data['address'],
        creator_id=1
    )
    new_order.save()

def register_individual_order(dp: Dispatcher):
    dp.register_message_handler(start_order, commands=['order'], state=['*'])
    dp.register_message_handler(order_number, state=[Order.number])
    dp.register_message_handler(order_surname, state=[Order.surname])
    dp.register_message_handler(order_phone, state=[Order.phone])
    dp.register_message_handler(order_choose_comment,
                                lambda message: message.text in ['Оставить комментарий', 'Продолжить'],
                                state=Order.choose_comment)
    dp.register_message_handler(order_comment, state=Order.comment)
    dp.register_message_handler(order_choose_delivery,
                                lambda message: message.text in ['До пункта выдачи', 'До двери'],
                                state=Order.choose_delivery)
    dp.register_message_handler(order_delivery_address, state=Order.address)
    dp.register_message_handler(order_confirm,
                                lambda message: message.text in ['Да, информация верна', 'Нет, начать заного'],
                                state=Order.confirm)
    dp.register_message_handler(order_error, state=[Order.confirm, Order.choose_delivery, Order.choose_comment])
