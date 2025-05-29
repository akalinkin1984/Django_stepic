import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


# class LoginUserForm(forms.Form): # форма не связанная с моделью
#     # определяем поля для формы
#     username = forms.CharField(label='Логин',
#                                widget=forms.TextInput(attrs={'class': 'form-input'})) # widget - стиль оформления
#     password = forms.CharField(label='Пароль',
#                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class LoginUserForm(AuthenticationForm): # наследуем от AuthenticationForm
    # определяем поля для формы
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'})) # widget - стиль оформления
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model() # получить текущую модель юзера
        fields = ['username', 'password'] # поля которые следует отображать


# class RegisterUserForm(forms.ModelForm): # улучшим эту форму специальным классом для регистрации пользователей UserCreationForm
#     username = forms.CharField(label='Логин')
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
#     password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput()) # повтор пароля
#
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
#         labels = {'email': 'E-mail', 'first_name': 'Имя', 'last_name': 'Фамилия', } # метки для полей
#
#     def clean_password2(self): # валидатор для проверки совпадения введенных паролей
#         cd = self.cleaned_data # очищенные данные
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Пароли не совпадают')
#         return cd['password']
#
#     def clean_email(self): # валидатор для проверки email на уникальность
#         email = self.cleaned_data['email']
#         if get_user_model().objects.filter(email=email).exists(): # если в текущей модели юзера есть записи в БД с таким же email
#             raise forms.ValidationError('Такой E-mail уже существует')
#         return email


class RegisterUserForm(UserCreationForm): # обязательно использовать поля username, password1, password2
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'})) # повтор пароля

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {'email': 'E-mail', 'first_name': 'Имя', 'last_name': 'Фамилия'} # метки(названия при отображении) для полей
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'})
        } # укажем стили для полей

    def clean_email(self): # валидатор для проверки email на уникальность
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists(): # если в текущей модели юзера есть записи в БД с таким же email
            raise forms.ValidationError('Такой E-mail уже существует')
        return email


class ProfileUserForm(forms.ModelForm): # форма для профиля пользователя
    username = forms.CharField(disabled=True, label='Логин', # disabled=True - не сможем редактировать
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='E-mail',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year = datetime.date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'date_birth', 'first_name', 'last_name']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'})
        }


class UserPasswordChangeForm(PasswordChangeForm): # форма для редактирования пароля
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))
