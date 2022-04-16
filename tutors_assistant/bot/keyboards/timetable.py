from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards import callback_data_base_menu
from bot.standard_bot_answers import BUTTON_BACK

timetable_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BUTTON_BACK,
                callback_data=callback_data_base_menu.new(id=1, action="back"),
            )
        ]
    ]
)
