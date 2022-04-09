from django.db import models


class HomeWorkModule(models.Model):
    """
    Модуль домашнего задания
    """

    name = models.CharField(verbose_name="Модуль домашнего задания", max_length=200)
    description = models.TextField(verbose_name="Описание", max_length=200, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Модуль домашнего задания"
        verbose_name_plural = "Модули домашнего задания"
