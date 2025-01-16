from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Student, Subject
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *


from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')


from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        # Отримуємо логін та пароль з форми
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Спробуємо автентифікацію користувача
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Логін користувача в систему

            # Перевіряємо роль користувача
            if user.is_teacher:
                # Якщо це вчитель, перенаправляємо на сторінку викладача
                return redirect('teacher_dashboard')
            elif user.is_student:
                # Якщо це студент, перенаправляємо на сторінку студента
                return redirect('student_start')

        # У разі невдалого входу (логін/пароль неправильні) перенаправляємо на student_start
        return redirect('student_start')

    # Якщо запит не POST (наприклад, при відкритті форми)
    return render(request, 'login.html')



def user_logout(request):
    logout(request)
    return redirect('login')

from .models import Student, Class

from django.shortcuts import render, redirect
from .models import Student, Class

from django.shortcuts import render
from .models import Teacher, Class


def teacher_dashboard(request):
    # Отримання фіктивних класів і студентів для демонстрації
    classrooms = [
        {'name': '10-А', 'subject': 'Математика'},
        {'name': '11-Б', 'subject': 'Фізика'}
    ]
    students = [
        {'name': 'Іван Іваненко', 'classroom': '10-А'},
        {'name': 'Марія Петренко', 'classroom': '11-Б'}
    ]

    # Повертаємо сторінку для викладача
    return render(request, 'teacher_dashboard.html', {'classrooms': classrooms, 'students': students})


def class_view(request):
    if request.user.role == 'teacher':
        students = Student.objects.all()  # Отримуємо всіх студентів
        return render(request, 'class_view.html', {'students': students})
    return redirect('home')

@login_required
def student_detail(request, student_id):
    if request.user.role == 'teacher':
        student = Student.objects.get(id=student_id)
        grades = Notas.objects.filter(student=student)
        return render(request, 'student_detail.html', {'student': student, 'grades': grades})
    return redirect('home')


@login_required
def student_dashboard(request):
    if request.user.role == 'student':
        subjects = Subject.objects.all()
        return render(request, 'class_view.html', {'subjects': subjects})
    return redirect('home')


@login_required
def subject_view(request, subject_id):
    if request.user.role == 'student':
        subject = Subject.objects.get(id=subject_id)
        grades = Notas.objects.filter(student=request.user.student_profile, subject=subject)
        return render(request, 'subject_view.html', {'subject': subject, 'grades': grades})
    return redirect('home')



def delete_grade(request, pk):
    grade = Grade.objects.get(pk=pk)
    grade.delete()
    return redirect('home')




# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Notas  # Імпортуємо модель Nota
from mainapp.forms import NotaForm  # Імпортуємо форму для редагування оцінки (додамо форму далі)

# Функція для редагування оцінки
def edit_nota(request, pk):
    # Отримуємо об'єкт Nota за допомогою первинного ключа (pk)
    nota = get_object_or_404(Notas, pk=pk)

    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)  # Заповнюємо форму даними з об'єкта Nota
        if form.is_valid():
            form.save()  # Зберігаємо зміни
            return redirect('home')  # Перенаправляємо на головну сторінку після збереження
    else:
        form = NotaForm(instance=nota)  # Якщо метод GET, відображаємо форму для редагування

    return render(request, 'edit_nota.html', {'form': form})  # Повертаємо шаблон із формою


from django.contrib.auth.decorators import login_required
from django.shortcuts import render



from django.views.generic import ListView
from .models import Subject

from django.shortcuts import render, get_object_or_404
from .models import Student, Class


from django.shortcuts import render
from .models import Student


from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.shortcuts import render

def teacher_class_view(request):
    # Статичні дані про клас
    classroom = {'id': 1, 'name': '10A'}  # Ви можете змінити ці дані на потрібні
    students = [
        {'name': 'Іван Іванов', 'age': 16, 'grade': 'A'},
        {'name': 'Марія Петрова', 'age': 17, 'grade': 'B'},
        {'name': 'Олексій Сидоров', 'age': 16, 'grade': 'A'}
    ]

    return render(request, 'teacher_class_view.html', {'classroom': classroom, 'students': students})


def students_list_view(request):
    # Статичні дані про учнів
    students = [
        {'name': 'Іван Іванов', 'age': 16, 'grade': 'A'},
        {'name': 'Марія Петрова', 'age': 17, 'grade': 'B'},
        {'name': 'Олексій Сидоров', 'age': 16, 'grade': 'A'}
    ]

    return render(request, 'students_list.html', {'students': students})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Subject, Notas
from django.contrib.auth.decorators import login_required
from .forms import NotaForm



from django.shortcuts import render, redirect

def class_view(request):
    # Статичний список предметів
    subjects = [
        {'id': 1, 'name': 'Математика'},
        {'id': 2, 'name': 'Фізика'},
        {'id': 3, 'name': 'Історія'},
    ]

    # Перевірка, чи був натиск на предмет
    if request.method == 'POST':
        return redirect('grade_detail')

    # Відображаємо список предметів
    context = {
        'subjects': subjects
    }
    return render(request, 'class_view.html', context)

@login_required
def student_detail(request, student_id):
    if request.user.role == 'teacher':
        student = get_object_or_404(Student, id=student_id)
        subjects = Subject.objects.all()
        return render(request, 'student_detail.html', {'student': student, 'subjects': subjects})
    return redirect('home')


@login_required
def add_nota(request, student_id):

    if request.user.role == 'teacher':
        student = get_object_or_404(Student, id=student_id)


        teacher = get_object_or_404(Teacher, user=request.user)
        subjects = teacher.subjects.all()

        if request.method == 'POST':

            subject_id = request.POST.get('subject')
            grade = request.POST.get('grade')

            subject = get_object_or_404(Subject, id=subject_id)

            nota = Notas(student=student, teacher=teacher, subject=subject, grade=grade)
            nota.save()

            return redirect('teacher_class_view', class_id=student.classroom.id)

        return render(request, 'add_nota.html', {'student': student, 'subjects': subjects})

    return redirect('home')


from django.shortcuts import redirect

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Student, Subject, Notas


def set_grade(request):
    # Статичні дані про студентів, предмети та оцінки
    students = {
        1: {'name': 'Іван Іванов', 'class': '10A'},
        2: {'name': 'Марія Петрова', 'class': '10A'},
        3: {'name': 'Олексій Сидоров', 'class': '10B'},
    }

    subjects = {
        1: {'name': 'Математика'},
        2: {'name': 'Фізика'},
        3: {'name': 'Хімія'},
    }

    teacher_subjects = [{'id': 1, 'name': 'Математика'}, {'id': 2, 'name': 'Фізика'}]

    # Статичні дані для оцінок (зазначаємо учнів, їх предмети і оцінки)
    grades = {
        1: {'student': students[1], 'subject': subjects[1], 'grade': 'A'},
        2: {'student': students[2], 'subject': subjects[2], 'grade': 'B'},
    }

    if request.method == 'POST':
        # Отримуємо значення з форми
        student_id = int(request.POST.get('student'))
        subject_id = int(request.POST.get('subject'))
        grade_value = request.POST.get('grade')

        # Перевірка чи існує студент з таким id
        student = students.get(student_id)
        if not student:
            return HttpResponse("Студента не знайдено.", status=404)

        # Перевірка чи існує предмет
        subject = next((subj for subj in teacher_subjects if subj['id'] == subject_id), None)
        if not subject:
            return HttpResponse("Предмет не знайдений для цього вчителя.", status=404)

        # Створення оцінки для студенту (використовуємо статичні дані)
        grades[student_id] = {'student': student, 'subject': subject, 'grade': grade_value}
        return HttpResponse(f"Оцінку {grade_value} виставлено студенту {student['name']} з предмету {subject['name']}.")

    return HttpResponse("Метод не підтримується.", status=405)
@login_required
def teacher_start(request):
    if request.user.role == 'teacher':
        return render(request, 'teacher_start.html')
    return redirect('home')


def student_start(request):
    # Просто показуємо сторінку студенту без перевірки ролі
    return render(request, 'student_start.html')


def grade_detail(request):
    # Просто повертаємо статичний шаблон
    return render(request, 'grade_detail.html')

def chat_home(request):
    if request.user.is_teacher:
        messages = Message.objects.filter(recipient=request.user)
    else:
        teachers = User.objects.filter(groups__name='Teachers')
        return render(request, 'chat_list.html', {'teachers': teachers})

def chat_with_user(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return redirect('chat_with_user', user_id=user_id)

    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=request.user))
    ).order_by('timestamp')
    return render(request, 'chat_room.html', {'messages': messages, 'recipient': recipient})




def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Отримуємо роль (teacher/student) з форми

        # Створюємо користувача з хешованим паролем
        user = CustomUser(
            username=username,
            role=role,
            password=make_password(password)  # Хешуємо пароль перед збереженням
        )
        user.save()

        return redirect('login')  # Перенаправляємо на сторінку входу після реєстрації

    return render(request, 'register.html')


from django.shortcuts import render, redirect
from django.contrib import messages

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Перевірка на задані логін і пароль
        if username == '12082010' and password == '26271262':
            return redirect('teacher_dashboard')  # Перенаправлення на панель вчителя
        else:
            messages.error(request, 'Невірний логін або пароль. Спробуйте ще раз.')
            return redirect('home')  # Повернення на головну

    return render(request, 'teacher_login.html')

