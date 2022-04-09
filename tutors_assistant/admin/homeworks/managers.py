from django.db import models


class HomeWorkManager(models.Manager):
    """
    Менеджер домашних заданий
    """

    def active(self):
        """
        Активные домашние задания
        """
        return self.filter(active=True)
