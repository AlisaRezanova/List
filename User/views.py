from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomRegistrationForm, CustomAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


def registration_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                form.add_error('password2', 'Пароли не совпадают.')
            else:
                user = User.objects.create_user(username=username, password=password1)
                login(request, user)
                return redirect('/')
    else:
        form = CustomRegistrationForm
    return render(request, 'User/autorization.html', {'form': form})


class LogView(LoginView):
    template_name = 'User/login.html'
    form_class = CustomAuthenticationForm


def logout_view(request):
    logout(request)
    return redirect('Login')


@login_required
def see_profile(request):
    user = request.user
    info = {
        'name': None,
        'username': user.username,
        'password': user.password
    }
    return render(request, 'User/profile.html', info)



