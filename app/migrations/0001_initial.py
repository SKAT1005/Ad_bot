# Generated by Django 5.1.2 on 2024-10-17 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Имя пользователя')),
                ('role', models.CharField(max_length=16, verbose_name='Роль пользователя')),
                ('username', models.CharField(max_length=64, verbose_name='Ник пользователя')),
                ('marketplace', models.CharField(max_length=64, verbose_name='Маркетплейс')),
                ('category', models.CharField(max_length=256, verbose_name='Категории')),
                ('successes', models.CharField(max_length=512, verbose_name='Успехи')),
                ('about_as', models.CharField(max_length=512, verbose_name='О нас')),
                ('who', models.CharField(max_length=512, verbose_name='Кого ищем?')),
                ('is_check', models.BooleanField(default=False, verbose_name='Проверено ли объявление')),
                ('send_date', models.CharField(max_length=32, verbose_name='Дата и время отправки')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=32, verbose_name='Id чата пользователя')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Является ли пользователь админом')),
                ('ad', models.ManyToManyField(blank=True, to='app.ad', verbose_name='Объявления клиента')),
            ],
        ),
    ]
