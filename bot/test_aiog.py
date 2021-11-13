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


@dp.message_handler(commands=['order'])
async def start_order(message: types.Message):
    await message.reply(f'Введите номер заказа')
    await Order.number.set()


@dp.message_handler(state=Order.number)
async def order_number(message: types.Message, state: FSMContext):
    await message.reply('Введите Фамилию (заказчика)')
    await state.update_data(number=message.text)
    await Order.next()


@dp.message_handler(state=Order.surname)
async def order_name(message: types.Message, state: FSMContext):
    await message.reply('Введите Ваш номер мобильного телефона')
    await state.update_data(surname=message.text)
    await Order.next()


@dp.message_handler(state=Order.phone)
async def order_name(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    user_data = await state.get_data()
    await message.answer(user_data)
    await state.finish()

executor.start_polling(dp)