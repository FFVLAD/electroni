from django import forms
from .models import Notas

class NotaForm(forms.ModelForm):
    class Meta:
        model = Notas
        fields = ['student', 'teacher', 'subject', 'date', 'grade']  # Список існуючих полів у моделі



from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Ім'я користувача"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введіть ім'я користувача"}),
    )
    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Введіть пароль"}),
    )
