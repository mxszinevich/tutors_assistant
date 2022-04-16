from django.contrib import admin

from admin.homeworks.models import ResourceMaterials


class ResourceMaterialsInline(admin.TabularInline):
    model = ResourceMaterials
    extra = 0
