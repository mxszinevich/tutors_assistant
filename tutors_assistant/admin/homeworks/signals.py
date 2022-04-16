from typing import Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from admin.homeworks.models import HomeWork
from admin.utils import producer
from bot.standard_bot_answers import HOMEWORK_CREATE
from rabbitmq_utils import Message


@receiver(signal=post_save, sender=HomeWork)
def send_message_new_homework(
    sender: Type[HomeWork], instance: HomeWork, created: bool, **kwargs
):
    """
    Сигнал, срабатывабщий после сохранения модели экземпляра HomeWork
    """
    if created:
        message = Message(
            chat_id=instance.student.telegram_chat, message=HOMEWORK_CREATE
        )
        producer(message.to_str())
