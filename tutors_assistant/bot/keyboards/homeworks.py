from typing import List, Dict, Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.keyboards import callback_data_base_menu
from bot.standard_bot_answers import (
    BUTTON_BACK,
    BUTTON_ANSWER,
    HOMEWORK_STATUS_DONE,
    HOMEWORK_STATUS_NOT_COMPLETED,
)

callback_data_homeworks = CallbackData("homework", "id", "action")
callback_data_homework_answer = CallbackData("homework", "id", "action")


def get_answer_text_status(has_answer: bool) -> str:
    """
    Получение статуса домашнего задания
    """
    if has_answer:
        status = HOMEWORK_STATUS_DONE
    else:
        status = HOMEWORK_STATUS_NOT_COMPLETED
    return status


def get_homeworks_keyboard(homeworks: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """
    Генерация клавиатуры для домашних заданий
    """
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTON_BACK,
                callback_data=callback_data_base_menu.new(id=1, action="back"),
            )
        ]
    ]
    for homework in homeworks:
        has_answer_status: str = get_answer_text_status(homework["has_answer"])
        inline_keyboard.insert(
            0,
            [
                InlineKeyboardButton(
                    text=f'{has_answer_status}{homework["name"]}',
                    callback_data=callback_data_homeworks.new(
                        id=homework["id"], action="work_retrieve"
                    ),
                ),
            ],
        )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_homework_answer_keyboard(homework_id: int) -> InlineKeyboardMarkup:
    """
    Кнопка ответа на домашнее задание
    """
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTON_ANSWER,
                callback_data=callback_data_homework_answer.new(
                    id=homework_id, action="homework_answer"
                ),
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
