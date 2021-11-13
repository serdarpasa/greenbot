import os
import sys

import telebot
from telebot import types
import json

import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.expanduser(BASE_DIR)
if path not in sys.path:
    sys.path.insert(0, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenway.settings")
django.setup()
from bot.models import PersonalOrder


TOKEN = '2124163604:AAG36f9I074pcWDl3h9aSd2b4Yr06te2r2k'

bot = telebot.TeleBot(token=TOKEN)


class Order:
    def __init__(self, ):
        self.dic = {}

    def get_order(self, message, dic):
        dic['user_order'] = message.text
        msg = bot.reply_to(message, 'Введите имя')
        bot.register_next_step_handler(msg, self.get_name, dic)

    def get_name(self, message, dic):
        try:
            dic['user_name'] = message.text
            msg = bot.reply_to(message, 'Введите тел')
            bot.register_next_step_handler(msg, self.get_phone, dic)
        except Exception as e:
            print(e)

    def get_phone(self, message, dic):
        try:
            dic['user_tel'] = message.text
            msg = bot.reply_to(message, 'Введите адресс')
            bot.register_next_step_handler(msg, self.get_address, dic)
        except:
            pass

    def get_address(self, message, dic):
        try:
            dic['user_adress'] = message.text
            # new_order = PersonalOrder.objects.create(user_id=1)

            bot.reply_to(message, 'поддтвердите заказ:')

            markup = types.InlineKeyboardMarkup()
            button_yes = types.InlineKeyboardButton('Подтверждаю', callback_data='correct')
            button_no = types.InlineKeyboardButton('Нет, начать заного', callback_data='wrong')

            markup.row(button_yes, button_no)
            bot.send_message(message.chat.id, json.dumps(dic), reply_markup=markup)
        except:
            pass

    @bot.callback_query_handler(func=lambda call: True)  # обработка кнопки
    def handle_callback(call):
        if call.data == 'correct':
            new_order = PersonalOrder.objects.create(user_id=1)
            new_order.is_active = True
            new_order.save()
            bot.send_message(call.message.chat.id, 'Заказ подтвержден, менеджер с вами свяжется.')
        elif call.data == 'wrong':
            bot.send_message(call.message.chat.id, 'Заказ отменен.')
        bot.edit_message_reply_markup(message_id=call.message.id,
                                      chat_id=call.message.chat.id,
                                      reply_markup=None)
        bot.answer_callback_query(call.id)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'lets start')

    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton('F', callback_data='aaaaaaaaaaaaaaaaaaaaa')
    button_no = types.InlineKeyboardButton('D', callback_data='wqre')

    markup.row(button_yes, button_no)
    bot.send_message(message.chat.id, 'testing', reply_markup=markup)

@bot.message_handler(commands=['order'])
def start_order(message):
    order = Order()
    order.dic = {'status': False}
    msg = bot.reply_to(message, 'Введите номер заказа')
    bot.register_next_step_handler(msg, order.get_order, order.dic)


@bot.callback_query_handler(func=lambda call: True)  # обработка кнопки
def handle_callback(call):
    print('test_Clalback')

@bot.message_handler(func=lambda message: True)
def echo(message):
    print(message.text)
    bot.reply_to(message, 'ничего не понимаю')


print(PersonalOrder.objects.all().count())
# bot.infinity_polling()
bot.infinity_polling()
