from typing import Dict, Any, List

from aiogram.types import CallbackQuery, InputFile

from bot.db_api.django_async import get_student_resourses, get_student_resourse
from bot.filters import RegistrationFilter
from bot.keyboards import (
    callback_data_base_menu,
)
from bot.keyboards.resources import get_resources_keyboard, callback_data_resourses
from bot.loader import dp
from bot.standard_bot_answers import ANSWER_IS_EMPTY


@dp.callback_query_handler(
    callback_data_base_menu.filter(action="resources"), RegistrationFilter()
)
async def get_resourses(call: CallbackQuery, callback_data: dict):
    """
    Получение списка учебных материалов
    """
    resources: List[Dict[str, Any]] = await get_student_resourses(
        student_telegram_id=call.from_user.id
    )
    await call.answer()

    text = "📚" if resources else ANSWER_IS_EMPTY
    resources_keyboard = get_resources_keyboard(resources)

    await call.message.edit_text(text=text, reply_markup=resources_keyboard)


@dp.callback_query_handler(
    callback_data_resourses.filter(action="resource"), RegistrationFilter()
)
async def get_resourse(call: CallbackQuery, callback_data):
    """
    Получения учебного материала
    """
    resource: Dict[str, Any] = await get_student_resourse(
        student_telegram_id=call.from_user.id,
        resource_id=callback_data["id"],
    )
    await call.answer()
    message_text = f'{resource["name"]}\n{resource["url"]}'
    await call.message.edit_text(text=message_text)
    if resource["file"]:
        await call.message.answer_document(
            document=InputFile(path_or_bytesio=f'admin/media/{resource["file"]}')
        )
