from bot.loader import dp
from .registration import CheckRegistrationMiddleware

if __name__ == "bot.middlewares":
    dp.setup_middleware(CheckRegistrationMiddleware())
