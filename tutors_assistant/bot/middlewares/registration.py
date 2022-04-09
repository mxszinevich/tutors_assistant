from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import User, Message

from bot.db_api import has_student
from bot.loader import dp
from bot.standard_bot_answers import REGISTRATION_START, REGISTRATION_NAME
from bot.states import RegistrationState


class CheckRegistrationMiddleware(BaseMiddleware):
    """
    Проверка регистрации пользователя
    """

    async def on_pre_process_message(self, message: Message, data: dict):
        user: User = message.from_user
        if all(
            (
                not await has_student(telegram_id=user.id),
                not await dp.current_state(user=user.id).get_state(),
            )
        ):
            await message.answer(REGISTRATION_START)
            await message.answer(REGISTRATION_NAME)
            await RegistrationState.full_name.set()

            raise CancelHandler()
