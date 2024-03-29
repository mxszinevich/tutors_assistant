# Generated by Django 3.2.18 on 2023-04-04 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220504_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='telegram_chat',
            field=models.BigIntegerField(blank=True, verbose_name='Telegram chat_id'),
        ),
        migrations.AlterField(
            model_name='student',
            name='telegram_id',
            field=models.BigIntegerField(blank=True, verbose_name='Telegram id'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='telegram_chat',
            field=models.BigIntegerField(blank=True, verbose_name='Telegram chat_id'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='telegram_id',
            field=models.BigIntegerField(blank=True, verbose_name='Telegram id'),
        ),
    ]
