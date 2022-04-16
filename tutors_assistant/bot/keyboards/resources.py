from typing import Any, Dict, List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.keyboards import callback_data_base_menu
from bot.standard_bot_answers import BUTTON_BACK

callback_data_resourses = CallbackData("resourses", "id", "action")


def get_resources_keyboard(resources: List[Dict["str", Any]]) -> InlineKeyboardMarkup:
    """
    Получение клавиатуры для списка ресурсов
    """
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTON_BACK,
                callback_data=callback_data_base_menu.new(id=1, action="back"),
            )
        ]
    ]

    if resources:
        for resource in resources:
            inline_keyboard.insert(
                0,
                [
                    InlineKeyboardButton(
                        text=resource["name"],
                        callback_data=callback_data_resourses.new(
                            id=resource["id"], action="resource"
                        ),
                    )
                ],
            )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
