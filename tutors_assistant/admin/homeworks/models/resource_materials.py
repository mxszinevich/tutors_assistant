from django.db import models

from admin.homeworks.utils import get_directory_path
from admin.users.models import Student


class ResourceMaterials(models.Model):
    """
    Справочные материалы
    """

    student = models.ForeignKey(
        to=Student, verbose_name="Студент", on_delete=models.CASCADE
    )
    active = models.BooleanField(verbose_name="Активно", default=True)
    name = models.TextField(verbose_name="Название/Text")
    url = models.URLField(verbose_name="Ссылка", blank=True, null=True)
    file = models.FileField(
        verbose_name="Фаил", upload_to=get_directory_path, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Справочные материалы"
        verbose_name_plural = "Справочные материалы"
