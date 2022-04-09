from aiogram.dispatcher.filters.state import StatesGroup, State


class HomeworkAnswerState(StatesGroup):
    """
    Состояние для ответа на домашнее задание
    """

    start = State()
