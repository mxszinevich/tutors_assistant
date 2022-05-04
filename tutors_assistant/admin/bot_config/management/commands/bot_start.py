import logging

from aiogram.utils import executor
from django.core.management import BaseCommand

from bot.loader import dp
from bot.utils.on_startup import on_startup
from bot.states import RegistrationState, MenuState
from bot.middlewares import CheckRegistrationMiddleware
from bot.handlers import *
from logger_conf import handler


class Command(BaseCommand):
    """
    Старт телеграм бота
    """

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.info("start polling")
        executor.start_polling(dispatcher=dp, on_startup=on_startup)
