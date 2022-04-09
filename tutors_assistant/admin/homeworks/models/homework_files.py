from django.db import models

from admin.homeworks.models import HomeWork
from admin.homeworks.utils import get_directory_path


class HomeworkFiles(models.Model):
    """
    Файлы домашнего задания
    """

    homework = models.ForeignKey(
        HomeWork, verbose_name="Домашняя работа", on_delete=models.CASCADE
    )
    description = models.TextField(verbose_name="Задание", max_length=200, blank=True)
    file = models.FileField(
        verbose_name="Фаил", upload_to=get_directory_path, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.homework.name

    class Meta:
        verbose_name = "Фаил домашнего задания"
        verbose_name_plural = "Файлы домашнего задания"
