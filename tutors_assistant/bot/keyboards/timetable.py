from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards import callback_data_base_menu

timetable_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="<- Назад",
                callback_data=callback_data_base_menu.new(id=1, action="back"),
            )
        ]
    ]
)
