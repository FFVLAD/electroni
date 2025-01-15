from django.contrib import admin
from .models import CustomUser, Subject, Teacher, Student, Notas, Class, Message


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_is_teacher', 'get_is_student')

    def get_is_teacher(self, obj):
        return obj.is_teacher
    get_is_teacher.short_description = 'Is Teacher'
    get_is_teacher.boolean = True

    def get_is_student(self, obj):
        return obj.is_student
    get_is_student.short_description = 'Is Student'
    get_is_student.boolean = True


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'all_classes_access')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade')


@admin.register(Notas)
class NotasAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'subject', 'grade', 'date')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp')
