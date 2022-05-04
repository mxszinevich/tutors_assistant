from django.db import models


class Teacher(models.Model):
    """
    Преподаватель
    """

    # Personal Info
    full_name = models.CharField(verbose_name="Полное имя", max_length=200)
    email = models.EmailField(verbose_name="Email", max_length=200)
    # Telegram
    telegram_name = models.CharField(
        verbose_name="Telegram name", max_length=200, blank=True
    )
    telegram_id = models.IntegerField(verbose_name="Telegram id", blank=True)
    telegram_chat = models.IntegerField(verbose_name="Telegram chat_id", blank=True)
    # Yandex
    yadisk_token = models.CharField(verbose_name="Токен яндекс диска", max_length=200, blank=True)
    yadisk_root_folder_name = models.CharField(verbose_name="Название корневой директори", max_length=200, blank=True)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
