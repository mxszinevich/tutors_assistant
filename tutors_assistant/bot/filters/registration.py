from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.db_api import has_student


class StudentFilter(BoundFilter):
    """
    Фильтр, определяющий является ли пользователь студентом
    """

    async def check(self, message: types.Message) -> bool:
        return await has_student(telegram_id=message.from_user.id)


class SenderUserFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return not message.from_user.is_bot
