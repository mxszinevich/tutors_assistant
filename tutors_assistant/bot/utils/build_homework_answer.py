from typing import Union

from aiogram.types import PhotoSize, File, Document

from bot.db_api import create_homework_answer
from bot.loader import dp


async def building_homework_answer_file(
    homework_id: int,
    answer_file: Union[PhotoSize, Document, None] = None,
    answer_text: str = "",
):
    """
    Отправка файлов ответа на сохранение
    """
    answer_data = {
        "homework_id": homework_id,
        "answer_text": answer_text,
    }
    if answer_file:
        file: File = await dp.bot.get_file(file_id=answer_file.file_id)
        file_path = f"media/answer/files/{file.file_path.split('/')[-1]}"
        await answer_file.download(destination=file_path)
        answer_data.update(file_path=file_path)

    await create_homework_answer(**answer_data)