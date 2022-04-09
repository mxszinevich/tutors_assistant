from django.contrib import admin

from admin.homeworks.models import HomeWorkModule


@admin.register(HomeWorkModule)
class HomeWorkModuleAdmin(admin.ModelAdmin):
    pass
