from typing import List, Dict, Any

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import (
    CallbackQuery,
    InputFile,
    MediaGroup,
    InputMediaDocument,
    InputMedia,
    Message,
    ContentType,
    ChatActions,
)
from aiogram.utils import markdown
from django.db.utils import DatabaseError

from bot.db_api import (
    get_student_homeworks,
    get_homework,
    get_homework_files,
)
from bot.filters import RegistrationFilter
from bot.keyboards import get_homeworks_keyboard, callback_data_homeworks
from bot.keyboards.base_menu import callback_data_base_menu, base_meny_keyboard
from bot.keyboards.homeworks import (
    callback_data_homework_answer,
    get_homework_answer_keyboard,
)
from bot.loader import dp
from bot.standard_bot_answers import (
    ANSWER_DATA_NOT_EMPTY,
    ANSWER_HOMEWORKS_IS_EMPTY,
    ANSWER_BACKEND_ERROR,
    ANSWER_HOMEWORKS_FINISH,
    START_HOMEWORK_ANSWER,
    ANSWER_START_MESSAGE,
    MAIN_MENU_TITLE,
)
from bot.states import HomeworkAnswerState
from bot.utils import get_homework_text, building_homework_answer_file


@dp.callback_query_handler(
    callback_data_base_menu.filter(action="homeworks"), RegistrationFilter()
)
async def homeworks_list(call: CallbackQuery, callback_data: dict):
    """
    Отображение списка домашних заданий
    """
    homeworks: List[Dict[str, Any]] = await get_student_homeworks(
        student_telegram_id=call.from_user.id
    )
    await call.answer()
    if homeworks:
        await call.message.edit_text(
            text=ANSWER_DATA_NOT_EMPTY,
            reply_markup=get_homeworks_keyboard(homeworks),
        )
    else:
        await call.message.answer(ANSWER_HOMEWORKS_IS_EMPTY)


@dp.callback_query_handler(
    callback_data_base_menu.filter(action="back"), RegistrationFilter()
)
async def homework_back(call: CallbackQuery, callback_data: dict):
    """
    Назад в главное меню
    """
    await call.message.edit_text(text=MAIN_MENU_TITLE, reply_markup=base_meny_keyboard)


@dp.callback_query_handler(
    callback_data_homeworks.filter(action="work_retrieve"), RegistrationFilter()
)
async def homework(call: CallbackQuery, callback_data: dict):
    """
    Отображение домашнего задания
    """
    await call.answer()

    homework_id = callback_data["id"]
    try:
        homework: Dict[str, Any] = await get_homework(
            student_telegram_id=call.from_user.id, homework_id=homework_id
        )
        homework_files: List[Dict[str, Any]] = await get_homework_files(
            homework_id=homework_id
        )
    except (DatabaseError, TypeError):
        await call.message.answer(ANSWER_BACKEND_ERROR)
        raise CancelHandler()

    medias: List[InputMedia] = []
    for file in homework_files:
        if file["file"]:
            medias.append(
                InputMediaDocument(
                    media=InputFile(path_or_bytesio=f'admin/media/{file["file"]}'),
                    caption=markdown.text(markdown.hbold(file["description"])),
                )
            )
    homework_text: str = get_homework_text(homework)

    await call.message.edit_text(homework_text)
    if medias:
        await dp.bot.send_chat_action(
            chat_id=call.message.chat.id, action=ChatActions.UPLOAD_PHOTO
        )
        media_group = MediaGroup(medias=medias)
        await call.message.answer_media_group(media=media_group)
    await call.message.answer(
        text=ANSWER_START_MESSAGE,
        reply_markup=get_homework_answer_keyboard(homework_id),
    )


@dp.callback_query_handler(
    callback_data_homework_answer.filter(action="homework_answer"), RegistrationFilter()
)
async def start_homework_answer(call: CallbackQuery, callback_data: dict):
    """
    Начало ответа на домашнее задание
    """
    await call.answer()
    await call.message.edit_text(
        text=START_HOMEWORK_ANSWER,
    )
    await HomeworkAnswerState.start.set()
    await dp.current_state().update_data(homework_id=callback_data.get("id"))


@dp.message_handler(Command("finish"), state=HomeworkAnswerState.start)
async def get_homework_answer_finish(message: Message, state: FSMContext):
    """
    Получение ответа на домашнее задание
    """
    await message.answer(ANSWER_HOMEWORKS_FINISH)
    await state.reset_state(with_data=True)


@dp.message_handler(state=HomeworkAnswerState.start, content_types=ContentType.PHOTO)
@dp.message_handler(state=HomeworkAnswerState.start, content_types=ContentType.DOCUMENT)
@dp.message_handler(state=HomeworkAnswerState.start, content_types=ContentType.TEXT)
async def get_homework_answer(message: Message, state: FSMContext):
    """
    Сохранение ответа на домашнее задание
    """
    homework_id = (await state.get_data()).get("homework_id")
    answer_data = {
        "homework_id": homework_id,
        "answer_text": message.text or message.caption or "",
    }
    if message.photo:
        answer_data["answer_file"] = message.photo[-1]
    elif message.document:
        answer_data["answer_file"] = message.document

    await building_homework_answer_file(**answer_data)
