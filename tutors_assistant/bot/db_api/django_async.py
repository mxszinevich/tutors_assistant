from os.path import basename
from typing import List, Dict, Any, Optional

from asgiref.sync import sync_to_async
from django.core.exceptions import FieldError
from django.core.files import File
from django.db.models import Exists, OuterRef

from admin.homeworks.models import (
    HomeWork,
    HomeworkFiles,
    HomeworkAnswer,
    ResourceMaterials,
)
from admin.users.models import Student, Teacher
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
        .annotate(
            has_answer=Exists(HomeworkAnswer.objects.filter(homework=OuterRef("pk")))
        )
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
) -> int:
    """
    Сохранение ответа на задание
    """
    answer = HomeworkAnswer(homework_id=homework_id, description=answer_text)
    if file_path:
        answer.file.save(basename(file_path), content=File(open(file_path, "rb")))
    answer.save()
    return answer.id


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


@sync_to_async
def get_student_resourses(student_telegram_id: int) -> dict:
    """
    Получение дополнительных материалов студента
    """

    resourses = list(
        ResourceMaterials.objects.filter(
            student__telegram_id=student_telegram_id, active=True
        ).values()
    )
    return resourses


@sync_to_async
def get_student_resourse(student_telegram_id: int, resource_id: int) -> dict:
    """
    Получение экземпляра дополнительных материалов студента
    """

    resourse = dict(
        ResourceMaterials.objects.filter(
            student__telegram_id=student_telegram_id,
            id=resource_id,
            active=True,
        )
        .values()
        .first()
    )
    return resourse


@sync_to_async
def get_teacher_homework(homework_id: int) -> Dict[str, Any]:
    """
    Получение данных учителя домашнего задания
    """
    return dict(Teacher.objects.filter(homework=homework_id).values().first())


@sync_to_async
def get_student(*values, **filters) -> Dict[str, Any]:
    """
    Получение данных студента
    """

    return dict(Student.objects.filter(**filters).values(*values).first())


@sync_to_async
def get_homework_answer(**filter) -> HomeworkAnswer:
    """
    Получение ответа на домашнее задание
    """
    homework_answer = HomeworkAnswer.objects.filter(**filter).first()
    return homework_answer


@sync_to_async
def get_yandex_disk_data(teacher_id: int) -> dict:
    print(
        Teacher.objects.filter(id=teacher_id)
        .values("yadisk_token", "yadisk_root_folder_name")
        .first()
    )
    yandex_disk_data = dict(
        Teacher.objects.filter(id=teacher_id)
        .values("yadisk_token", "yadisk_root_folder_name")
        .first()
    )
    return yandex_disk_data
