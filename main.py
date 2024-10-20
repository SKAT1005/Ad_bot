import datetime
import os
import random
import threading
import time

import django
import telebot
from telebot.types import LabeledPrice

import buttons
from const import bot, admin_bot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ad_bot.settings')
django.setup()
from app.models import User, Ad
from django.utils import timezone


def send_ad():
    while True:
        n = timezone.now()
        if n.minute == 0:
            day = n.day
            month = n.month
            year = n.year
            hours = n.hour
            s = f"{day}.{month}.{year} {hours}:00"
            ads = Ad.objects.filter(date=s)
            for ad in ads:
                text = f'Имя: {ad.name}\n' \
                       f'Роль: {ad.role}\n' \
                       f'Ник в телеграмм: {ad.username}\n' \
                       f'Маркетплейс: {ad.marketplace}\n' \
                       f'Категория: {ad.category}\n' \
                       f'Достижения: {ad.successes}\n' \
                       f'О нас: {ad.about_as}\n' \
                       f'Кого ищем: {ad.who}'
                bot.send_message(chat_id='-1002120671637', text=text)
            time.sleep(60 * 60)
        else:
            time.sleep(60)


def enter_who(message, chat_id, user, name, role, username, marketplace, category, successes, about_as):
    if message.content_type == 'text':
        who = message.text
        ad = Ad.objects.create(
            name=name,
            role=role,
            username=username,
            marketplace=marketplace,
            category=category,
            successes=successes,
            about_as=about_as,
            who=who
        )
        user.ad.add(ad)
        text = f'Имя: {name}\n' \
               f'Роль: {role}\n' \
               f'Ник в телеграмм: {username}\n' \
               f'Маркетплейс: {marketplace}\n' \
               f'Категория: {category}\n' \
               f'Достижения: {successes}\n' \
               f'О нас: {about_as}\n' \
               f'Кого ищем: {who}'
        prices = [LabeledPrice(label="XTR", amount=1)]
        bot.send_invoice(chat_id=chat_id,
                         title='Оплата рекламы',
                         description=text,
                         prices=prices,
                         currency='XTR',
                         invoice_payload='channel_support',
                         provider_token='',
                         reply_markup=buttons.pay(ad.id))


def enter_about_as(message, chat_id, user, name, role, username, marketplace, category, successes):
    if message.content_type == 'text':
        about_as = message.text
        text = '8/9. ▪️Какого селлера и компанию вы ищете, опишите их\n\n' \
               'Пример ответа:\n\n' \
               '— опыт необязателен\n' \
               '— своевременные поставки товара\n' \
               '— работа в системе учета\n' \
               '— своевременная оплата\n' \
               '— возможность роста в зп'
        msg = bot.send_message(chat_id=chat_id, text=text)
        bot.register_next_step_handler(msg, enter_who, chat_id, user, name, role, username, marketplace, category,
                                       successes, about_as)


def enter_successes(message, chat_id, user, name, role, username, marketplace, category):
    if message.content_type == 'text':
        successes = message.text
        text = '7/9. ▪️Расскажите о себе\n\n' \
               'Пример ответа:\n\n' \
               '📍Работаю 2 года\n' \
               '📍Удаленная работа\n' \
               '📍Владение фотошопом (ссылка на примеры работ)'
        msg = bot.send_message(chat_id=chat_id, text=text)
        bot.register_next_step_handler(msg, enter_about_as, chat_id, user, name, role, username, marketplace, category,
                                       successes)


def enter_category(message, chat_id, user, name, role, username, marketplace):
    if message.content_type == 'text':
        category = message.text
        text = '6/9. 💰Поделитесь своими успехами\n\n' \
               'Пример ответа: \n\n' \
               '— развил магазин с 100 000 рублей до 1 200 000 рублей за 3 месяца\n' \
               '— магазина 1 000 000 выручки в месяц'
        msg = bot.send_message(chat_id=chat_id, text=text)
        bot.register_next_step_handler(msg, enter_successes, chat_id, user, name, role, username, marketplace, category)


def enter_marketplace(message, chat_id, user, name, role, username):
    if message.content_type == 'text':
        marketplace = message.text
        text = '5/9. Введите категории товаров'
        msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=None)
        bot.register_next_step_handler(msg, enter_category, chat_id, user, name, role, username, marketplace)


def enter_username(message, chat_id, user, name, role):
    if message.content_type == 'text':
        username = message.text
        text = '4/9. Выберите маркетплейс или введите свой'
        msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.choose_marketplace())
        bot.register_next_step_handler(msg, enter_marketplace, chat_id, user, name, role, username)


def enter_role(message, chat_id, user, name):
    if message.content_type == 'text':
        role = message.text
        if role not in ['Менеджер', 'Селлер']:
            msg = bot.send_message(chat_id=chat_id, text='Выберите роль из кнопок под клавиатурой',
                                   reply_markup=buttons.choose_role())
            bot.register_next_step_handler(msg, enter_role, chat_id, user, name)
        else:
            text = '3/9. Введите ник в телеграм для связи\n\n' \
                   'Пример ответа:\n\n' \
                   '@redmilliard'
            msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=None)
            bot.register_next_step_handler(msg, enter_username, chat_id, user, name, role)


def enter_name(message, chat_id, user):
    if message.content_type == 'text':
        name = message.text
        text = '2/9. Вы менеджер или селлер\n\n' \
               'Нажмите на нужную кнопку'
        msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons.choose_role())
        bot.register_next_step_handler(msg, enter_role, chat_id, user, name)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user, _ = User.objects.get_or_create(chat_id=chat_id)
    menu(chat_id=chat_id, user=user)


def menu(chat_id, user):
    pay = user.ad.all()
    text = 'Здравствуйте!\n\n' \
           f'Оплачено объявлений — {pay.count()}\n' \
           f'Опубликовано/запланировано объявлений — {pay.filter(is_check=True).count()}\n\n' \
           'Чтобы разместить объявление, ответьте, пожалуйста, на вопросы:\n\n' \
           '1/9. Введите ваше имя'
    msg = bot.send_message(chat_id=chat_id, text=text)
    bot.register_next_step_handler(msg, enter_name, chat_id, user)


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    chat_id = message.chat.id
    user = User.objects.get(chat_id=chat_id)
    ad = user.ad.last()
    admin = random.choice(User.objects.filter(is_admin=True))
    try:
        bot.delete_message(chat_id=chat_id, message_id=message.id)
    except Exception:
        pass
    text = f'Имя: {ad.name}\n' \
           f'Роль: {ad.role}\n' \
           f'Ник в телеграмм: {ad.username}\n' \
           f'Маркетплейс: {ad.marketplace}\n' \
           f'Категория: {ad.category}\n' \
           f'Достижения: {ad.successes}\n' \
           f'О нас: {ad.about_as}\n' \
           f'Кого ищем: {ad.who}'
    admin_bot.send_message(chat_id=admin.chat_id, text=text,
                           reply_markup=buttons.admin_buttons(user_id=user.chat_id, ad_id=ad.id))


@admin_bot.message_handler(commands=['start'])
def admin_start(message):
    if User.objects.filter(chat_id=message.chat.id, is_admin=True):
        admin_bot.send_message(chat_id=message.chat.id, text='Вы успешно авторизовались, ожидайте заявок')


def choose_date(chat_id, ad_id):
    bot.send_message(chat_id=chat_id, text='Ваше объявление одобрено, выдерите дату отправки сообщения',
                     reply_markup=buttons.choose_date(ad_id=ad_id))


@admin_bot.callback_query_handler(func=lambda call: True)
def callback(call):
    message_id = call.message.id
    chat_id = call.message.chat.id
    try:
        admin_bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass
    try:
        admin_bot.delete_message(chat_id=chat_id, message_id=message_id - 1)
    except Exception:
        pass
    if call.message:
        data = call.data.split('|')
        if data[0] == 'accept':
            choose_date(chat_id=data[1], ad_id=data[2])


def choose_time(chat_id, date, ad_id):
    bot.send_message(chat_id=chat_id, text='Выберите время отправки сообщения',
                     reply_markup=buttons.choose_time(date=date, ad_id=ad_id))


def set_send_time(chat_id, time, ad_id):
    ad = Ad.objects.get(id=ad_id)
    ad.send_date = time
    ad.save(update_fields=['send_date'])
    bot.send_message(chat_id=chat_id, text=f'Ваше объявление будет опубликовано {time}')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    message_id = call.message.id
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user = User.objects.filter(chat_id=user_id).first()
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        pass
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id - 1)
    except Exception:
        pass
    if call.message:
        data = call.data.split('|')
        bot.clear_step_handler_by_chat_id(chat_id=chat_id)
        msg = bot.send_message(chat_id=chat_id, text='.', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.delete_message(chat_id=chat_id, message_id=msg.id)
        if data[0] == 'change':
            try:
                Ad.objects.get(id=data[1]).delete()
            except Exception:
                pass
            menu(chat_id=chat_id, user=user)
        elif data[0] == 'date':
            choose_time(chat_id=chat_id, date=data[1], ad_id=data[2])
        elif data[0] == 'time':
            set_send_time(chat_id=chat_id, time=data[1], ad_id=data[2])


def run_user_bot():
    bot.polling(none_stop=True)


def run_admin_bot():
    admin_bot.polling(none_stop=True)


if __name__ == '__main__':
    run_user_bot = threading.Thread(target=run_user_bot)
    run_user_bot.start()
    run_admin_bot = threading.Thread(target=run_admin_bot)
    run_admin_bot.start()
    send_ad = threading.Thread(target=send_ad)
    send_ad.start()
