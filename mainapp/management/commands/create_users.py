from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mainapp.models import StudentProfile, TeacherProfile  # Замініть шлях до ваших моделей, якщо потрібно
import random

CustomUser = get_user_model()


class Command(BaseCommand):
    help = "Створення профілів для користувачів, включаючи 80 учнів і 4 вчителів"

    def handle(self, *args, **kwargs):
        # Генерація 80 учнів
        self.stdout.write("Генерація 80 учнів...")
        student_first_names = [f"Ім'яУчня{i}" for i in range(1, 81)]
        student_last_names = [f"ПрізвищеУчня{i}" for i in range(1, 81)]

        for i in range(80):
            username = f"student{i + 1}"
            email = f"student{i + 1}@example.com"
            first_name = student_first_names[i]
            last_name = student_last_names[i]

            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'student',  # Якщо у вас є поле role
                }
            )
            if created:
                user.set_password('1234')
                user.save()
                StudentProfile.objects.create(user=user)  # Створюємо профіль студента
                self.stdout.write(f"Створено учня: {username}")

        # Генерація 4 вчителів
        self.stdout.write("Генерація 4 вчителів...")
        teacher_first_names = [f"Ім'яВчителя{i}" for i in range(1, 5)]
        teacher_last_names = [f"ПрізвищеВчителя{i}" for i in range(1, 5)]

        for i in range(4):
            username = f"teacher{i + 1}"
            email = f"teacher{i + 1}@example.com"
            first_name = teacher_first_names[i]
            last_name = teacher_last_names[i]

            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'teacher',  # Якщо у вас є поле role
                }
            )
            if created:
                user.set_password('1234')
                user.save()
                TeacherProfile.objects.create(user=user)  # Створюємо профіль вчителя
                self.stdout.write(f"Створено вчителя: {username}")

        self.stdout.write("Успішно завершено!")
