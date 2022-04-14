from django.apps import AppConfig


class HomeworkConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin.homeworks"
    verbose_name = "Домашние задания"

    def ready(self):
        from admin.homeworks.signals import send_message_new_homework
