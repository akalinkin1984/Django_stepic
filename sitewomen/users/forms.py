from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


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


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput()) # повтор пароля

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        labels = {'email': 'E-mail', 'first_name': 'Имя', 'last_name': 'Фамилия', } # метки для полей

    def clean_password2(self): # валидатор для проверки совпадения введенных паролей
        cd = self.cleaned_data # очищенные данные
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password']

    def clean_email(self): # валидатор для проверки email на уникальность
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists(): # если в текущей модели юзера есть записи в БД с таким же email
            raise forms.ValidationError('Такой E-mail уже существует')
        return email
