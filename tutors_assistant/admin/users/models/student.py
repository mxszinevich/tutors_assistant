from django.db import models

from admin.users.models import Teacher


class Student(models.Model):
    """
    Студент
    """

    # Personal Info
    full_name = models.CharField(verbose_name="Полное имя", max_length=200)
    email = models.EmailField(verbose_name="Email", max_length=200)
    # Learning
    teacher = models.ForeignKey(
        to=Teacher,
        verbose_name="Учитель",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    subject = models.CharField(
        verbose_name="Предмет занятий", blank=True, max_length=200
    )
    # Telegram
    telegram_name = models.CharField(
        verbose_name="Telegram name", max_length=200, blank=True
    )
    telegram_id = models.IntegerField(verbose_name="Telegram id", blank=True)
    telegram_chat = models.IntegerField(verbose_name="Telegram chat_id", blank=True)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
