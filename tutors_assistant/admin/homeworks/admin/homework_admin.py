from django.contrib import admin

from admin.homeworks.admin import HomeworkFilesInline, HomeWorkAnswerInline
from admin.homeworks.models import HomeWork


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    readonly_fields = ("count_days_delay",)
    inlines = [HomeWorkAnswerInline, HomeworkFilesInline]
    list_display = ("__str__", "student", "final_day", "score", "active")
