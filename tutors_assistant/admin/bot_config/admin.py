from django.contrib import admin

from admin.bot_config.models import TelegramBot


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    pass
