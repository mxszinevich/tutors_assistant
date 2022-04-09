from aiogram import Dispatcher
from aiogram.types import BotCommand


async def on_startup(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            BotCommand("start", "Запустить бота"),
            BotCommand("menu", "Меню"),
        ]
    )
