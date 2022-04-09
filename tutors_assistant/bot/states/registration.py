from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationState(StatesGroup):
    """
    Регистрация пользователя
    """

    full_name = State()
    email = State()
    subject = State()
