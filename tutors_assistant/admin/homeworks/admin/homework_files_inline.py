from django.contrib import admin

from admin.homeworks.models import HomeworkFiles


class HomeworkFilesInline(admin.TabularInline):
    model = HomeworkFiles
    extra = 0
