from django import forms


class LoginUserForm(forms.Form): # форма не связанная с моделью
    # определяем поля для формы
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'})) # widget - стиль оформления
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))