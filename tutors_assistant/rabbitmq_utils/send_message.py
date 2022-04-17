from aiogram import Dispatcher

from rabbitmq_utils import Message


async def chat_send_message(dp: Dispatcher, message: Message):
    """
    Отправка сообщений в чат
    """
    if message.type == Message.TYPE_TEXT:
        await dp.bot.send_message(
            chat_id=message.chat_id, text=message.message
        )

