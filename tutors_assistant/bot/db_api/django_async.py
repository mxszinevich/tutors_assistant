from os.path import basename
from typing import List, Dict, Any, Optional

from asgiref.sync import sync_to_async
from django.core.exceptions import FieldError
from django.core.files import File
from django.db.models import Exists, OuterRef

from admin.homeworks.models import HomeWork, HomeworkFiles, HomeworkAnswer
from admin.users.models import Student
from admin.users.models.sudent_timetable import StudentTimeTable


@sync_to_async
def has_student(**filter_params) -> bool:
    """
    Проверка существования ученика
    """
    try:
        return Student.objects.filter(**filter_params).exists()
    except FieldError:
        return False


@sync_to_async
def create_student(**student_data) -> Student:
    """
    Создание ученика
    """
    try:
        return Student.objects.create(**student_data)
    except TypeError:
        return False


@sync_to_async
def get_student_homeworks(student_telegram_id: int, **fields) -> List[Dict[str, Any]]:
    """
    Получение списка домашних заданий
    """
    return list(
        HomeWork.objects.active()
        .filter(student__telegram_id=student_telegram_id)
        .annotate(
            has_answer=Exists(HomeworkAnswer.objects.filter(homework=OuterRef("pk")))
        )
        .values(**fields)
    )


@sync_to_async
def get_homework(student_telegram_id: int, homework_id: int) -> Dict[str, Any]:
    """
    Получение домашнего задания
    """
    return dict(
        HomeWork.objects.active()
        .filter(student__telegram_id=student_telegram_id, id=homework_id)
        .values()
        .first()
    )


@sync_to_async
def get_homework_files(homework_id: int) -> List[Dict[str, Any]]:
    files: List[Dict[str, Any]] = list(
        HomeworkFiles.objects.filter(homework_id=homework_id).values()
    )
    return files


@sync_to_async
def create_homework_answer(
    homework_id: int, file_path: Optional[str] = None, answer_text: str = ""
):
    """
    Сохранение ответа на задание
    """
    answer = HomeworkAnswer(homework_id=homework_id, description=answer_text)
    if file_path:
        answer.file.save(basename(file_path), content=File(open(file_path, "rb")))
    answer.save()


@sync_to_async
def get_student_timetable(student_telegram_id: int) -> dict:
    """
    Получение расписания студента
    """
    timetable = list(
        StudentTimeTable.objects.filter(
            student__telegram_id=student_telegram_id
        ).values()
    )
    return timetable
