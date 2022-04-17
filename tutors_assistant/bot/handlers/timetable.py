from typing import Dict, Any

from aiogram.types import CallbackQuery

from bot.db_api.django_async import get_student_timetable
from bot.filters import StudentFilter
from bot.keyboards import (
    callback_data_base_menu,
    timetable_keyboard,
    base_meny_keyboard,
)
from bot.loader import dp
from bot.standard_bot_answers import ANSWER_IS_EMPTY, MAIN_MENU_TITLE


@dp.callback_query_handler(
    callback_data_base_menu.filter(action="back"), StudentFilter()
)
async def timetable_back(call: CallbackQuery, callback_data: dict):
    """
    Назад в главное меню
    """
    await call.message.edit_text(text=MAIN_MENU_TITLE, reply_markup=base_meny_keyboard)


@dp.callback_query_handler(
    callback_data_base_menu.filter(action="timetable"), StudentFilter()
)
async def get_timetable(call: CallbackQuery, callback_data: dict):
    """
    Получение расписания занятий
    """
    timetable: Dict[str, Any] = await get_student_timetable(
        student_telegram_id=call.from_user.id
    )
    await call.answer()
    if timetable:
        text_timetable = []
        for time in timetable:
            text_timetable.append(time["time_table_text"])

        await call.message.edit_text(
            "\n".join(text_timetable), reply_markup=timetable_keyboard
        )
    else:
        await call.message.edit_text(
            text=ANSWER_IS_EMPTY, reply_markup=timetable_keyboard
        )
