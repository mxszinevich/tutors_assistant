from django.contrib import admin

from admin.users.models import User, Student, Teacher
from admin.users.models.sudent_timetable import StudentTimeTable


class StudentTimeTableInline(admin.TabularInline):
    """
    Расписание занятий студента
    """

    model = StudentTimeTable
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentTimeTableInline]
