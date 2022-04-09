from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from admin.homeworks.managers import HomeWorkManager
from admin.users.models import Student
from admin.homeworks.models import HomeWorkModule


class HomeWork(models.Model):
    """
    Домашнее задание
    """

    objects = HomeWorkManager()

    student = models.ForeignKey(
        to=Student, verbose_name="Студент", on_delete=models.CASCADE
    )
    module = models.ForeignKey(
        to=HomeWorkModule, verbose_name="Модуль задания", on_delete=models.CASCADE
    )

    name = models.TextField(verbose_name="Название домашнего задания", max_length=300)
    description = models.TextField(verbose_name="Описание", max_length=500, blank=True)

    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )
    final_day = models.DateTimeField(
        verbose_name="Последний день сдачи задания",
    )
    active = models.BooleanField(verbose_name="Задание активно", default=True)
    count_days_delay = models.PositiveSmallIntegerField(
        verbose_name="Количество дней опоздания", default=0
    )

    def __str__(self) -> str:
        return (
            f"{self.student.full_name} "
            f"- {self.name} "
            f"- {self.final_day.strftime('%A, %d. %B %Y %I:%M%p') if self.final_day else ''}"
        )

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
