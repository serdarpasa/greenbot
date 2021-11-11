import os
import sys

import telebot
from telebot import types
import json



TOKEN = '2124163604:AAG36f9I074pcWDl3h9aSd2b4Yr06te2r2k'

bot = telebot.TeleBot(token=TOKEN)


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
    dic = {'status': False}
    msg = bot.reply_to(message, 'Введите номер заказа')
    bot.register_next_step_handler(msg, get_order, dic)


def get_order(message, dic):
    dic['user_order'] = message.text
    msg = bot.reply_to(message, 'Введите имя')
    bot.register_next_step_handler(msg, get_name, dic)


def get_name(message, dic):
    try:
        dic['user_name'] = message.text
        msg = bot.reply_to(message, 'Введите тел')
        bot.register_next_step_handler(msg, get_phone, dic)
    except Exception as e:
        print(e)


def get_phone(message, dic):
    try:
        dic['user_tel'] = message.text
        msg = bot.reply_to(message, 'Введите адресс')
        bot.register_next_step_handler(msg, get_address, dic)
    except:
        pass


def get_address(message, dic):
    try:
        dic['user_adress'] = message.text

        bot.reply_to(message, 'поддтвердите заказ:')

        markup = types.InlineKeyboardMarkup()
        button_yes = types.InlineKeyboardButton('Подтверждаю', callback_data='data_correct')
        button_no = types.InlineKeyboardButton('Нет, начать заного', callback_data='data_wrong')

        markup.row(button_yes, button_no)
        bot.send_message(message.chat.id, json.dumps(dic), reply_markup=markup)
    except:
        pass


@bot.callback_query_handler(func=lambda call: True)  # обработка кнопки
def handle_callback(call):
    if call.data == 'data_correct':
        print(call.message)
        bot.send_message(call.message.chat.id, 'Заказ подтвержден, менеджер с вами свяжется.')
    elif call.data == 'data_wrong':
        bot.send_message(call.message.chat.id, 'Заказ отменен.')
    bot.edit_message_reply_markup(message_id=call.message.id,
                                  chat_id=call.message.chat.id,
                                  reply_markup=None)
    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda message: True)
def echo(message):
    print(message.text)
    bot.reply_to(message, 'ничего не понимаю')

bot.infinity_polling()