from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.db_api import has_student


class RegistrationFilter(BoundFilter):
    """
    Фильтр, определяющий зарегистрирован ли пользователь
    """

    async def check(self, message: types.Message) -> bool:
        return await has_student(telegram_id=message.from_user.id)


class SenderUserFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return not message.from_user.is_bot
