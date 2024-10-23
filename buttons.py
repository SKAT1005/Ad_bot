import datetime
import os

import django
from django.utils import timezone
from telebot import types

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ad_bot.settings')
django.setup()
from app.models import User, Ad


def choose_role():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    markup.row('Менеджер', 'Селлер', 'Начать сначала')
    return markup


def choose_marketplace():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    markup.row('WILDBERRIES', 'Ozon', 'Яндекс Маркет', 'Начать сначала')
    return markup


def pay(id, user):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton(text='Оплатить и отправить на модерацию', pay=True)
    if user.bonus >= 1799:
        pay = types.InlineKeyboardButton(text='Оплатить баллами и отправить на модерацию', callback_data=f'pay|{id}')
        markup.add(pay)
    change = types.InlineKeyboardButton(text='Изменить', callback_data=f"change|{id}")
    markup.add(btn, change)
    return markup


def choose_date(ad_id):
    markup = types.InlineKeyboardMarkup(row_width=4)
    n = [timezone.now() + datetime.timedelta(days=x) for x in range(14)]
    weekday = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }
    for i in n:
        date = types.InlineKeyboardButton(text=f'{i.day}.{i.month} {weekday[i.weekday()]}', callback_data=f'date|{i.day}.{i.month}.{i.year}|{ad_id}')
        markup.add(date)
    return markup


def choose_time(date, ad_id):
    markup = types.InlineKeyboardMarkup(row_width=4)
    back = types.InlineKeyboardButton('Вернуться к выбору даты', callback_data=f'back|{ad_id}')
    markup.add(back)
    for i in range(8, 24):
        time_date = f'{date} {i}:00'
        if not Ad.objects.filter(send_date=time_date).first():
            time = types.InlineKeyboardButton(text=f'{i}:00', callback_data=f'time|{time_date}|{ad_id}')
            markup.add(time)
    return markup


def admin_buttons(user_id, ad_id):
    markup = types.InlineKeyboardMarkup()
    accept = types.InlineKeyboardButton(text='Одобрить', callback_data=f'accept|{user_id}|{ad_id}')
    cansel = types.InlineKeyboardButton(text='Отклонить', callback_data='cansel')
    markup.add(accept, cansel)
    return markup


def menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    create_ad = types.InlineKeyboardButton(text='Опубликовать объявление', callback_data='create_ad')
    get_invite_link = types.InlineKeyboardButton(text='Получить ссылку для приглашения друзей', callback_data='get_invite_link')
    get_my_stats = types.InlineKeyboardButton(text='Узнать мой баланс', callback_data='get_my_stats')
    markup.add(create_ad, get_invite_link, get_my_stats)
    return markup


def start_over():
    markup = types.InlineKeyboardMarkup(row_width=1)
    create_ad = types.InlineKeyboardButton(text='Начать сначала', callback_data='create_ad')
    markup.add(create_ad)
    return markup