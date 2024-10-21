from django.db import models

class User(models.Model):
    chat_id = models.CharField(max_length=32, verbose_name='Id чата пользователя')
    ad = models.ManyToManyField('Ad', blank=True, verbose_name='Объявления клиента')
    is_admin = models.BooleanField(default=False, verbose_name='Является ли пользователь админом')
    invite_link = models.CharField(max_length=64, blank=True, null=True, verbose_name='Ссылка приглашение')
    invite_user = models.IntegerField(default=0, verbose_name='Кол-во приглашенных пользователей')
    bonus = models.IntegerField(default=0, verbose_name='Кол-во бонусов пользователя')



class Ad(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя пользователя')
    role = models.CharField(max_length=16, verbose_name='Роль пользователя')
    username = models.CharField(max_length=64, verbose_name='Ник пользователя')
    marketplace = models.CharField(max_length=64, verbose_name='Маркетплейс')
    category = models.CharField(max_length=256, verbose_name='Категории')
    successes = models.CharField(max_length=512, verbose_name='Успехи')
    about_as = models.CharField(max_length=512, verbose_name='О нас')
    who = models.CharField(max_length=512, verbose_name='Кого ищем?')
    is_check = models.BooleanField(default=False, verbose_name='Проверено ли объявление')
    send_date = models.CharField(max_length=32, verbose_name='Дата и время отправки')