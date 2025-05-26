from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginUserForm


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])  # выполняем аутентификацию пользователя(проверяем есть ли юзер в БД)
            if user and user.is_active:
                login(request, user) # выполняем авторизацию(вход в систему)
                return HttpResponseRedirect(reverse('home')) # перенаправляем на главную страницу

    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request) # выполняем выход из системы
    return HttpResponseRedirect(reverse('users:login')) # перенаправляем на страницу авторизации
