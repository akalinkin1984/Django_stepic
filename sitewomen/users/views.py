from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from sitewomen import settings
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


# Create your views here.
# def login_user(request): # перепишем эту функцию с помощью класса LoginView
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])  # выполняем аутентификацию пользователя(проверяем есть ли юзер в БД)
#             if user and user.is_active:
#                 login(request, user) # выполняем авторизацию(вход в систему)
#                 return HttpResponseRedirect(reverse('home')) # перенаправляем на главную страницу
#
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})


class LoginUser(LoginView):
    # form_class = AuthenticationForm # класс формы, если нужно использовать свою форму LoginUserForm, то нужно ее унаследовать от AuthenticationForm
    form_class = LoginUserForm
    template_name = 'users/login.html' # имя шаблона
    extra_context = {'title': 'Авторизация'} # дополнительные параметры

    # def get_success_url(self): # переопределяем стандартный путь перенаправления при успешной авторизации, или можно
    #     # в файле settings.py определить следующие переменные:
    #     # LOGIN_REDIRECT_URL – задает URL - адрес, на который следует перенаправлять пользователя после успешной авторизации;
    #     # LOGIN_URL – определяет URL - адрес, на который следует перенаправить неавторизованного пользователя при попытке посетить закрытую страницу сайта;
    #     # LOGOUT_REDIRECT_URL – задает URL - адрес, на который перенаправляется пользователь после выхода.
    #     return reverse_lazy('home')


# def logout_user(request): # вместо этой функции, прямо в пути в файле url.py, прописали класс LogoutView
#     logout(request) # выполняем выход из системы
#     return HttpResponseRedirect(reverse('users:login')) # перенаправляем на страницу авторизации


# def register(request): # перепишем эту функцию с помощью класса CreateView
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password']) # формирование и шифрование пароля
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login') # куда перенаправлять при успешной регистрации


class ProfileUser(LoginRequiredMixin, UpdateView): # класс для обработки профиля пользователя(LoginRequiredMixin - только для аутентифицированных пользователей)
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': 'Профиль пользователя',
        'default_image': settings.DEFAULT_USER_IMAGE
    }

    def get_success_url(self): # куда перенаправлять если есть изменения и сохранение
        return reverse_lazy('users:profile') # перенаправляем на текущую страницу

    def get_object(self, queryset=None): # для редактирования только своей записи
        return self.request.user


class UserPasswordChange(PasswordChangeView): # для изменения пароля
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
