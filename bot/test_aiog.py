from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


TOKEN = '2124163604:AAG36f9I074pcWDl3h9aSd2b4Yr06te2r2k'
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Hello world')


class Order(StatesGroup):
    number = State()
    surname = State()
    phone = State()
    want_comment = State()
    comment = State()
    delivery = State()


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

    # keyboard = types.InlineKeyboardMarkup()
    # button_yes = types.InlineKeyboardButton('Оставить комментарий', callback_data='leave_comment')
    # button_no = types.InlineKeyboardButton('Продолжить', callback_data='continue')
    # keyboard.add(button_yes, button_no)
    # await message.answer('Хотите оставить комментарий?', reply_markup=keyboard)

    keyboard = types.ReplyKeyboardMarkup()
    button_yes = types.KeyboardButton('Оставить комментарий')
    button_no = types.KeyboardButton('Продолжить')
    keyboard.add(button_yes, button_no)
    await message.answer("Хотите оставить коментарий?", reply_markup=keyboard)
    await Order.next()


@dp.message_handler(state=Order.want_comment)
async def order_whant_comment(message: types.Message, state: FSMContext):
    if message.text == 'Оставить комментарий':
        print('YES')
        await message.answer('Введите свой комментайрий:')
        await Order.next()
    elif message.text == 'Продолжить':
        print('NO')
        await message.answer('Выберите тип доставки')
        await state.update_data(comment=None)
        await Order.delivery.set()
    else:
        pass


@dp.message_handler(state=Order.comment)
async def order_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await message.answer('Выберите тип доставки')
    await Order.next()

# async def get_comment(message: types.Message, status):
#     if status:
#         print('yes')
#         await message.answer('Введите свой комментарий:')
#         print(message.text)
#         await Order.next()
#     else:
#         await message.answer('Выберите тип доставки')
#         await Order.delivery.set()



# @dp.callback_query_handler(text='leave_comment')
# async def leave_comment(message: types.Message):
#     print(f'leave com: {message.text}')
#     await state.update_data(message.text)
#     await Order.next()
#     # обработка inline-button


@dp.message_handler(state=Order.delivery)
async def order_delivery(message: types.Message, state: FSMContext):
    print(f'del {message.text}')
    user_data = await state.get_data()
    print(user_data)
    await message.answer('fff')

    await state.finish()
    # await message.reply('Выберите тип доставки')



executor.start_polling(dp)