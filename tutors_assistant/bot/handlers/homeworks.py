import json
import logging
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
)
from aiogram.utils import markdown
from django.db.utils import DatabaseError

from admin.config.settings import MEDIA_ROOT
from admin.utils import producer
from bot.db_api import (
    get_student_homeworks,
    get_homework,
    get_homework_files,
)
from bot.db_api.django_async import get_teacher_homework, get_student
from bot.filters import StudentFilter
from bot.keyboards import get_homeworks_keyboard, callback_data_homeworks
from bot.keyboards.base_menu import callback_data_base_menu, base_meny_keyboard
from bot.keyboards.homeworks import (
    callback_data_homework_answer,
    get_homework_answer_keyboard,
)
from bot.loader import dp, redis
from bot.standard_bot_answers import (
    ANSWER_DATA_NOT_EMPTY,
    ANSWER_HOMEWORKS_IS_EMPTY,
    ANSWER_BACKEND_ERROR,
    ANSWER_HOMEWORKS_FINISH,
    START_HOMEWORK_ANSWER,
    ANSWER_START_MESSAGE,
    MAIN_MENU_TITLE,
    HOMEWORK_STUDENT_ANSWERED,
)
from bot.states import HomeworkAnswerState
from bot.utils import get_homework_text, building_homework_answer_file
from logger_conf import handler
from rabbitmq_utils import Message as r_Message

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@dp.callback_query_handler(
    callback_data_base_menu.filter(action="homeworks"), StudentFilter()
)
async def homeworks_list(call: CallbackQuery, callback_data: dict):
    """
    Отображение списка домашних заданий
    """

    logger.info(f"homeworks_list: student_telegram_id={call.from_user.id}")

    if redis.get(name=f"homeworks_{call.from_user.id}"):
        homeworks: List[Dict[str, Any]] = json.loads(
            redis.get(name=f"homeworks_{call.from_user.id}")
        )
    else:
        homeworks: List[Dict[str, Any]] = await get_student_homeworks(
            student_telegram_id=call.from_user.id
        )
        redis.setex(
            name=f"homeworks_{call.from_user.id}",
            time=60,
            value=json.dumps(homeworks, default=str),
        )

    await call.answer()
    homeworks_keyboard = get_homeworks_keyboard(homeworks)
    homeworks_text = ANSWER_HOMEWORKS_IS_EMPTY
    if homeworks:
        homeworks_text = ANSWER_DATA_NOT_EMPTY
    logger.info(
        f"homeworks_list: student_telegram_id={call.from_user.id}: edit_text={homeworks_text}"
    )
    await call.message.edit_text(text=homeworks_text, reply_markup=homeworks_keyboard)


@dp.callback_query_handler(
    callback_data_base_menu.filter(action="back"), StudentFilter()
)
async def homework_back(call: CallbackQuery, callback_data: dict):
    """
    Назад в главное меню
    """
    await call.message.edit_text(text=MAIN_MENU_TITLE, reply_markup=base_meny_keyboard)


@dp.callback_query_handler(
    callback_data_homeworks.filter(action="work_retrieve"), StudentFilter()
)
async def homework(call: CallbackQuery, callback_data: dict):
    """
    Отображение домашнего задания
    """
    await call.answer()
    homework_id = callback_data["id"]
    logger.info(
        f"homework: student_telegram_id={call.from_user.id}: homework_id={homework_id}"
    )
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
                    media=InputFile(path_or_bytesio=f'{MEDIA_ROOT}/{file["file"]}'),
                    caption=markdown.text(markdown.hbold(file["description"])),
                )
            )
    homework_text: str = get_homework_text(homework)
    logger.info(
        f"homework: student_telegram_id={call.from_user.id}: homework_id={homework_id}"
    )
    await call.message.edit_text(homework_text)
    if medias:
        media_group = MediaGroup(medias=medias)
        await call.message.answer_media_group(media=media_group)
        logger.info(
            f"homework: student_telegram_id={call.from_user.id}: homework_id={homework_id}: media{media_group.to_python()}"
        )
    await call.message.answer(
        text=ANSWER_START_MESSAGE,
        reply_markup=get_homework_answer_keyboard(homework_id),
    )


@dp.callback_query_handler(
    callback_data_homework_answer.filter(action="homework_answer"), StudentFilter()
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
    logger.info(
        f"start_homework_answer: student_telegram_id={call.from_user.id}: homework_id={callback_data.get('id')}"
    )
    await dp.current_state().update_data(homework_id=callback_data.get("id"))


@dp.message_handler(Command("finish"), state=HomeworkAnswerState.start)
async def get_homework_answer_finish(message: Message, state: FSMContext):
    """
    Получение ответа на домашнее задание
    """
    await message.answer(ANSWER_HOMEWORKS_FINISH)
    await state.reset_state(with_data=True)


@dp.message_handler(
    StudentFilter(), state=HomeworkAnswerState.start, content_types=ContentType.PHOTO
)
@dp.message_handler(
    StudentFilter(), state=HomeworkAnswerState.start, content_types=ContentType.DOCUMENT
)
@dp.message_handler(
    StudentFilter(), state=HomeworkAnswerState.start, content_types=ContentType.TEXT
)
async def get_homework_answer(message: Message, state: FSMContext):
    """
    Сохранение ответа на домашнее задание
    """
    homework_id = (await state.get_data()).get("homework_id")
    answer_data = {
        "student_telegram_id": message.from_user.id,
        "homework_id": homework_id,
        "answer_text": message.text or message.caption or "",
    }
    logger.info(
        f"get_homework_answer: student_telegram_id={message.from_user.id}: homework_id={homework_id}"
    )
    if message.photo:
        answer_data["answer_file"] = message.photo[-1]
    elif message.document:
        answer_data["answer_file"] = message.document

    if not (
        (
            await get_homework(
                student_telegram_id=message.from_user.id, homework_id=homework_id
            )
        )["has_answer"]
    ):
        teacher: Dict[str, Any] = await get_teacher_homework(homework_id=homework_id)
        student_message_info = "full_name"
        student_full_name: Dict[str, Any] = await get_student(
            student_message_info, telegram_id=message.from_user.id
        )
        message = r_Message(
            chat_id=teacher["telegram_chat"],
            message=HOMEWORK_STUDENT_ANSWERED(
                student_full_name=student_full_name[student_message_info]
            ),
            type=r_Message.TYPE_TEXT,
            homework_id=homework_id,
        )
        producer(message.to_str())
        logger.info(
            f"get_homework_answer: rabbitmq message_send: {teacher['telegram_chat']}: homework_id= {homework_id}"
        )

    await building_homework_answer_file(**answer_data)
