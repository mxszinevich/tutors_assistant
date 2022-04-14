from aiogram.utils import executor
from django.core.management import BaseCommand

from bot.loader import dp
from bot.utils.on_startup import on_startup

# States
from bot.states import RegistrationState, MenuState

# Middleware
from bot.middlewares import CheckRegistrationMiddleware

# Handlers
from bot.handlers import *


class Command(BaseCommand):
    """
    Старт телеграм бота
    """

    def handle(self, *args, **options):
        executor.start_polling(dispatcher=dp, on_startup=on_startup)
