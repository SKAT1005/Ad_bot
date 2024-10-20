import datetime

from django.utils import timezone
from telebot import types


def choose_role():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    markup.row('Менеджер', 'Селлер')
    return markup


def choose_marketplace():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    markup.row('WILDBERRIES', 'Ozon', 'Яндекс Маркет')
    return markup


def pay(id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton(text='Оплатить и отправить на модерацию', pay=True)
    change = types.InlineKeyboardButton(text='Изменить', callback_data=f"change|{id}")
    markup.add(btn, change)
    return markup


def choose_date(ad_id):
    markup = types.InlineKeyboardMarkup(row_width=4)
    n = [timezone.now() + datetime.timedelta(days=x) for x in range(14)]

    for i in n:
        date = types.InlineKeyboardButton(text=f'{i.day}.{i.month}', callback_data=f'date|{i.day}.{i.month}.{i.year}|{ad_id}')
        markup.add(date)
    return markup


def choose_time(date, ad_id):
    markup = types.InlineKeyboardMarkup(row_width=4)
    for i in range(8, 24):
        time = types.InlineKeyboardButton(text=f'{i}:00', callback_data=f'time|{date} {i}:00|{ad_id}')
        markup.row(time)
    return markup


def admin_buttons(user_id, ad_id):
    markup = types.InlineKeyboardMarkup()
    accept = types.InlineKeyboardButton(text='Одобрить', callback_data=f'accept|{user_id}|{ad_id}')
    cansel = types.InlineKeyboardButton(text='Отклонить', callback_data='cansel')
    markup.add(accept, cansel)
    return markup
