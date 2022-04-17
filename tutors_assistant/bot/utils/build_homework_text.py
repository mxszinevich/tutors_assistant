from dataclasses import dataclass
from datetime import date
from typing import Optional
from django.utils import dateformat

from aiogram.utils import markdown


@dataclass
class HomeworkField:
    """
    Модель поля описания домашнего задания
    """

    field: str
    help_text: str = ""
    html_attribute: Optional[str] = None


def set_text_extra_params(field_data: str, homework_field: HomeworkField) -> str:
    """
    Установка дополнительный параметров для поля в описании домашнего задания
    """

    if homework_field.html_attribute is not None:
        field_data = getattr(markdown, homework_field.html_attribute)(field_data)
    if homework_field.help_text:
        field_data = "\n".join([markdown.hbold(homework_field.help_text), field_data])

    return field_data


def set_type_format(field_data: str) -> str:
    """
    Форматирование поля в зависимости от типа
    """
    if isinstance(field_data, date):
        field_data = dateformat.format(field_data, "d M Y")

    return field_data


def get_homework_text(homework: dict) -> str:
    homework_text = "А тут ничего нет 🙉"
    if homework:
        fields = [
            HomeworkField(
                field="name", html_attribute="hunderline", help_text="Название:"
            ),
            HomeworkField(field="description", help_text="Описание: ✍"),
            HomeworkField(field="final_day", help_text="Сдать до: ⏱"),
        ]
        homework_data = []
        for homework_field in fields:
            if homework_field.field in homework:
                field_data = homework[homework_field.field]

                if field_data:
                    field_data = set_type_format(field_data)
                    field_data = set_text_extra_params(field_data, homework_field)
                homework_data.append(field_data)

        homework_text = markdown.text(*homework_data, sep="\n\n")

    return homework_text
