import logging
from typing import Dict

from aiogram import types
from aiogram.dispatcher import FSMContext
from validate_email import validate_email

from bot.db_api import create_student
from bot.filters import SenderUserFilter
from bot.loader import dp
from bot.standard_bot_answers import (
    REGISTRATION_EMAIL,
    REGISTRATION_SUBJECT,
    REGISTRATION_INVALID_EMAIL,
    REGISTRATION_FINISH,
    REGISTRATION_INVALID,
)
from bot.states import RegistrationState

logger = logging.getLogger(__name__)


@dp.message_handler(SenderUserFilter(), state=RegistrationState.full_name)
async def get_student_full_name(message: types.Message, state: FSMContext):
    """
    Сохранение имени студента
    """

    full_name = message.text.strip()
    logger.info(f"get_student_full_name: {full_name}")
    await state.update_data(full_name=full_name)
    await message.answer(REGISTRATION_EMAIL)
    await state.set_state(RegistrationState.email)


@dp.message_handler(SenderUserFilter(), state=RegistrationState.email)
async def get_student_email(message: types.Message, state: FSMContext):
    """
    Сохранение emailа студента
    """
    email = message.text.strip()
    logger.info(f"get_student_email: {email}")
    if validate_email(email=email):
        await state.update_data(email=email)
        await message.answer(REGISTRATION_SUBJECT)
        await state.set_state(RegistrationState.subject)
    else:
        await message.answer(REGISTRATION_INVALID_EMAIL)


@dp.message_handler(SenderUserFilter(), state=RegistrationState.subject)
async def get_student_subject(message: types.Message, state: FSMContext):
    """
    Сохранение предмета занятия студента и окончание регистрации
    """
    subject = message.text.strip()
    await state.update_data(subject=subject)

    data: Dict = await state.get_data()
    user = message.from_user
    data.update(
        telegram_id=user.id, telegram_name=user.full_name, telegram_chat=message.chat.id
    )
    logger.info(f"get_student_subject: {subject}")
    logger.info(
        f"get_student_subject.user:  telegram_id={user.id}, telegram_name={user.full_name}, telegram_chat={message.chat.id}"
    )
    student = await create_student(**data)

    if student:
        await message.answer(REGISTRATION_FINISH)
        await state.reset_state(with_data=True)
    else:
        await message.answer(REGISTRATION_INVALID)
