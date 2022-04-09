from django.db import models

from admin.homeworks.models import HomeWork
from admin.homeworks.utils import get_directory_path


class HomeworkAnswer(models.Model):
    """
    Ответ на домашнее задание
    """

    homework = models.ForeignKey(
        HomeWork,
        verbose_name="Домашняя работа",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name="Задание", max_length=200, blank=True)
    file = models.FileField(
        verbose_name="Фаил", upload_to=get_directory_path, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.id}"

    class Meta:
        verbose_name = "Ответ на домашнее задание"
        verbose_name_plural = "Ответы на домашнее задание"
