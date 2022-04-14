import os

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from admin.bot_config.models import TelegramBot

bot_db = TelegramBot.objects.all().first() or os.getenv("BOT_TOKEN")
bot = Bot(token=bot_db.token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
