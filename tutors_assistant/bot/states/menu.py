from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuState(StatesGroup):
    """
    Состояния для основного меню бота

    base_menu - основное меню
    homework - домашние работы
    next_lesson - следующее занятие
    evaluations - оценки
    """

    base_menu = State()
    homework = State()
    next_lesson = State()
    evaluations = State()
