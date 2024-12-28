from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="", max_length=20, widget=forms.TextInput(attrs={
        'class': '',
        'placeholder': 'Логин',
    }))
    password = forms.CharField(label="", strip=False, max_length=20, widget=forms.PasswordInput(attrs={
        'class': '',
        'placeholder': "Пароль",
    }))


class CustomRegistrationForm(forms.Form):
    username = forms.CharField(label="", max_length=20, widget=forms.TextInput(attrs={
        'class': '',
        'placeholder': 'Логин',
    }))
    password1 = forms.CharField(label="", max_length=20, widget=forms.PasswordInput(attrs={
        'class': '',
        'placeholder': "Пароль",
    }))
    password2 = forms.CharField(label="", max_length=20, widget=forms.PasswordInput(attrs={
        'class': '',
        'placeholder': "Пароль",
    }))