from django.contrib import admin

from admin.homeworks.models import HomeworkAnswer


class HomeWorkAnswerInline(admin.TabularInline):
    model = HomeworkAnswer
    extra = 0
