import logging
from typing import Optional

from httpx import Response

from bot.db_api.django_async import get_student, get_homework, get_yandex_disk_data
from bot.utils.yandex import yandex_disk_create_folder
from bot.utils.yandex.send_document import yandex_disk_send_documents
from logger_conf import handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


async def sender_homework_answer_to_yandex_disk(
    student_telegram_id,
    homework_id: int,
    file_path: Optional[str] = None,
    answer_text: str = "",
):
    """
    Отправка файлов ответа на домашнего задания на яндекс диск
    """
    homework: dict = await get_homework(
        student_telegram_id=student_telegram_id, homework_id=homework_id
    )
    logger.info(f"sender_homework_answer_to_yandex_disk:" f"homework_id={homework_id} ")

    student_data: dict = await get_student(telegram_id=student_telegram_id)
    yandex_disk_data: dict = await get_yandex_disk_data(
        teacher_id=student_data["teacher_id"]
    )
    if yandex_disk_data["yadisk_token"]:
        token = yandex_disk_data["yadisk_token"]
        root_folder_name = yandex_disk_data["yadisk_root_folder_name"] or "homework"
        folder_path = (
            f"{root_folder_name}/{student_data['full_name']}/{homework['name']}/"
        )
        response: Response = await yandex_disk_create_folder(
            path=folder_path, token=token
        )
        if response.status_code in [201, 409]:
            await yandex_disk_send_documents(
                folder_path=folder_path,
                file_path=file_path,
                token=token,
            )
