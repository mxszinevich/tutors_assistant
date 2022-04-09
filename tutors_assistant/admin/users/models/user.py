from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    """
    Администратор системы
    """

    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
