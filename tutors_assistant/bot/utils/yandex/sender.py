from typing import Optional

from httpx import Response

from bot.db_api.django_async import get_student, get_homework
from bot.utils.yandex import yandex_disk_create_folder
from bot.utils.yandex.send_document import yandex_disk_send_documents


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
    student_data: dict = await get_student(telegram_id=student_telegram_id)
    folder_path = f"homework/{student_data['full_name']}/{homework['name']}/"
    response: Response = await yandex_disk_create_folder(path=folder_path)

    if response.status_code in [201, 409]:
        await yandex_disk_send_documents(
            folder_path=folder_path,
            file_path=file_path,
        )
