from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin.bot_config"
    verbose_name = "Телеграм бот"
