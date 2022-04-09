from aiogram import types
from aiogram.dispatcher.filters import Command

from bot.filters import RegistrationFilter
from bot.keyboards import base_meny_keyboard, callback_data_base_menu
from bot.loader import dp
from bot.standard_bot_answers import MAIN_MENU_TITLE


@dp.message_handler(Command("menu"), RegistrationFilter(), state="*")
async def show_menu(message: types.Message):
    """
    Отображение базового меню
    """
    await message.answer(MAIN_MENU_TITLE, reply_markup=base_meny_keyboard)
    if await dp.current_state().get_state():
        await dp.current_state().reset_state(with_data=True)
