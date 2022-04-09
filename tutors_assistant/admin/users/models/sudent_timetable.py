from django.db import models
from admin.users.models import Student


class StudentTimeTable(models.Model):
    """
    Расписание занятий
    """

    DAYS = (
        (1, "Понедельник"),
        (2, "Вторник"),
        (3, "Среда"),
        (4, "Четверг"),
        (5, "Пятница"),
        (6, "Суббота"),
        (7, "Воскресенье"),
    )
    student = models.ForeignKey(
        Student, verbose_name="Студент", on_delete=models.CASCADE, null=True, blank=True
    )
    time_table_text = models.CharField(
        verbose_name="Расписание занятий", max_length=200
    )
    time_table_day = models.PositiveSmallIntegerField(
        verbose_name="День недели", choices=DAYS
    )
    time_table_time = models.TimeField(verbose_name="Время занятия")

    class Meta:
        verbose_name = "Расписание занятий"
        verbose_name_plural = "Расписания занятий"

    def __str__(self) -> str:
        return self.time_table_text
