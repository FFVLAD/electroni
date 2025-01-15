from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Student, Subject
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')


from django.contrib.auth import authenticate, login


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Визначити URL залежно від ролі
            if user.role == 'teacher':
                redirect_url = '/teacher_dashboard/'  # Сторінка для вчителів
            elif user.role == 'student':
                redirect_url = '/student_start/'  # Сторінка для студентів
            else:
                redirect_url = '/'  # У випадку невідомої ролі

            # Показати сторінку завантаження
            return render(request, 'loading.html', {'redirect_url': redirect_url})
        else:
            return HttpResponse("Невірний логін або пароль")
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

from .models import Student, Class

from django.shortcuts import render, redirect
from .models import Student, Class

def teacher_dashboard(request):
    if request.user.role == 'teacher':

        classrooms = Class.objects.filter(teacher=request.user)


        students = Student.objects.filter(classroom__teacher=request.user)

        for student in students:
            student.grades_list = student.grades.all()
        return render(request, 'teacher_dashboard.html', {'classrooms': classrooms, 'students': students})
    return redirect('home')


@login_required
def class_view(request, grade):
    if request.user.role == 'teacher':
        students = Student.objects.filter(grade=grade)
        return render(request, 'class_view.html', {'students': students, 'grade': grade})
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
from .models import Class, Student, Notas, Subject

def teacher_class_view(request, class_id):
    classroom = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(classroom=classroom)

    return render(request, 'teacher_class_view.html', {'classroom': classroom, 'students': students})


def students_list_view(request):
    # Отримуємо всіх учнів з бази даних
    students = Student.objects.all()

    # Передаємо список учнів у шаблон
    return render(request, 'students_list.html', {'students': students})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Subject, Notas
from django.contrib.auth.decorators import login_required
from .forms import NotaForm



@login_required
def class_view(request, grade):
    if request.user.role == 'teacher':

        students = Student.objects.filter(grade=grade)
        return render(request, 'class_view.html', {'students': students, 'grade': grade})
    return redirect('home')



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


def set_grade(request, student_id):
    if not hasattr(request.user, 'teacher'):
        return HttpResponse("У вас немає доступу до цієї функції.", status=403)

    teacher_profile = request.user.teacherprofile
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        grade_value = request.POST.get('grade')

        subject = get_object_or_404(teacher_profile.subjects, id=subject_id)
        grade = Notas.objects.create(student=student, subject=subject, value=grade_value, teacher=request.user)
        return HttpResponse("Оцінку виставлено успішно!")





@login_required
def teacher_start(request):
    if request.user.role == 'teacher':
        return render(request, 'teacher_start.html')
    return redirect('home')


def student_start(request):
    if request.user.is_authenticated and request.user.is_student:
        return render(request, 'student_start.html')  # Головна сторінка студента
    else:
        return render(request, 'error.html', {'message': 'Доступ заборонено!'})

def grade_detail(request, grade_id):
    grade = get_object_or_404(Notas, id=grade_id)
    return render(request, 'grade_detail.html', {'grade': grade})


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


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        TeacherProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_teacher_profile(sender, instance, **kwargs):
    if hasattr(instance, 'teacherprofile'):
        instance.teacherprofile.save()


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import StudentProfile  # Замініть на ваш шлях до моделі

CustomUser = get_user_model()

@receiver(post_save, sender=CustomUser)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        # Перевірте, чи користувач має роль студента (якщо це необхідно)
        if instance.role == 'student':
            StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_student_profile(sender, instance, **kwargs):
    if hasattr(instance, 'student_profile'):
        instance.student_profile.save()



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Аутентифікація користувача
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Логін користувача
            if user.is_teacher:
                return redirect('teacher_start')  # Якщо це вчитель
            elif user.is_student:
                return redirect('student_start')  # Якщо це студент
        else:
            messages.error(request, 'Неправильний логін або пароль!')
            return redirect('student_start')  # Якщо логін або пароль неправильні

    return render(request, 'login.html')  # Форма логіну
