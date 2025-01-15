"""
URL configuration for electroni project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import viewsЪ



    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainapp import views  # Correct import
from django.contrib.auth import views as auth_views
from mainapp.forms import CustomLoginForm
from django.urls import path
from mainapp import views
from django.urls import path
from django.contrib.auth.views import LoginView
from mainapp import views
from django.contrib import admin
from django.urls import path
from mainapp import views  # Замість `mainapp` вкажіть назву вашого додатку


from django.contrib import admin
from django.urls import path
from mainapp import views  # Імпортуйте ваші views

urlpatterns = [
    # Головна сторінка
    path('', views.home, name='home'),  # Домашня сторінка

    # Сторінки для старту
    path('teacher_start/', views.teacher_start, name='teacher_start'),  # Для вчителів
    path('student_start/', views.student_start, name='student_start'),  # Для студентів
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),  # Панель вчителя

    # Клас з оцінками
    path('class_view/<int:grade>/', views.class_view, name='class_view'),  # Оцінки за класом

    # Аутентифікація
    path('login/', views.user_login, name='login'),  # Вхід до системи
    path('logout/', views.user_logout, name='logout'),  # Вихід із системи

    # Клас для вчителів
    path('teacher_class_view/<int:class_id>/', views.teacher_class_view, name='teacher_class_view'),  # Перегляд класу

    # Оцінки
    path('set_grade/<int:student_id>/', views.set_grade, name='set_grade'),  # Встановлення оцінки
    path('grade_detail/<int:grade_id>/', views.grade_detail, name='grade_detail'),  # Деталі оцінки

    # Чат
    path('chat/', views.chat_home, name='chat_room'),  # Головна сторінка чату
    path('chat/<int:user_id>/', views.chat_with_user, name='chat_with_user'),  # Чат із користувачем

    # Адмін-панель
    path('admin/', admin.site.urls),  # Адмін-панель
]

