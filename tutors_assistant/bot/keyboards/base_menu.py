from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

callback_data_base_menu = CallbackData("base_menu", "id", "action")

base_meny_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Домашние задания 👻",
                callback_data=callback_data_base_menu.new(id=1, action="homeworks"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Расписание занятий ⏳",
                callback_data=callback_data_base_menu.new(id=2, action="timetable"),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Учебные материалы 📚",
                callback_data=callback_data_base_menu.new(id=3, action="resources"),
            ),
        ],
    ]
)
