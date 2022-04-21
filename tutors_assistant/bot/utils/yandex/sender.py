from typing import Optional

from bot.db_api.django_async import get_student
from bot.utils.yandex import yandex_disk_create_folder


async def sender_homework_answer_to_yandex_disk(
    student_telegram_id,
    homework_id: int,
    file_path: Optional[str] = None,
    answer_text: str = "",
):
    """
    Отправка файлов ответа на домашнего задания на яндекс диск
    """

    student_data: dict = await get_student(telegram_id=student_telegram_id)
    folder_path = f"homework/{student_data['full_name']}"
    await yandex_disk_create_folder(path=folder_path)
