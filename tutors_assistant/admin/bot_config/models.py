from django.db import models
from singleton_model import SingletonModel


class TelegramBot(SingletonModel):
    """
    Телеграм бот
    """

    name = models.CharField(verbose_name="Имя", max_length=100)
    token = models.CharField(verbose_name="Токен", max_length=300)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Бот"
        verbose_name_plural = "Бот"
