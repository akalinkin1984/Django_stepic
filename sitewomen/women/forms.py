from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


# @deconstructible
# class RussianValidator: # определяем свой валидатор на проверку допустимых символов(ALLOWED_CHARS)
#     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
#     code = 'russian'
#
#     def __init__(self, message=None):
#         self.message = message if message else 'Должны присутствовать только русские символы, дефис и пробел.'
#
#     def __call__(self, value, *args, **kwargs):
#         if not(set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)


# class AddPostForm(forms.Form): # определяем класс для отображения формы не связанной с моделью
#     title = forms.CharField(max_length=255, min_length=5,
#                             label='Заголовок',
#                             widget=forms.TextInput(attrs={'class': 'form-input'}),
#                             # validators=[
#                             #     RussianValidator()
#                             # ],
#                             error_messages={ # установливаем свои сообщения об ошибках
#                                 'min_length': 'Слишком короткий заголовок',
#                                 'required': 'Без заголовка никак'
#                             }) # в widget указываем class для данного поля
#     slug = forms.SlugField(max_length=255, label='URL',
#                            validators=[ # указываем валидаторы
#                                MinLengthValidator(5, message='Минимум 5 символов'), # стандартный валидатор на проверку минимальной длины поля
#                                MaxLengthValidator(100, message='Максимум 100 символов'), # стандартный валидатор на проверку максимальной длины поля
#                            ])
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент') # многострочный текст с указание размера поля, required - необязательное поле
#     is_published = forms.BooleanField(required=False, initial=True, label='Статус')
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категории не выбраны', label='Категории') # выпадающий список
#     husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label='Не замужем', required=False, label='Муж') # выпадающий список
#
#     def clean_title(self): # метод для проверки поля title, указываем название поля через_(вместо объявления своего валидатора)
#         title = self.cleaned_data['title'] # получаем значение title
#         ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
#
#         if not(set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError('Должны присутствовать только русские символы, дефис и пробел.')


class AddPostForm(forms.ModelForm): # определяем класс для отображения формы связанной с моделью
    # у объекта появляется метод save для сохранения в БД
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label='Категории не выбраны',
                                 label='Категории')  # выпадающий список, указываем явно, чтобы отображалось empty_label

    husband = forms.ModelChoiceField(queryset=Husband.objects.all(),
                                     empty_label='Не замужем',
                                     required=False,
                                     label='Муж') # выпадающий список, указываем явно, чтобы отображалось empty_label

    class Meta:
        model = Women # указываем с какой моделью связать
        fields = ['title', 'slug', 'content', 'photo',
                  'is_published', 'cat', 'husband', 'tags'] # указываем поля, которые будут отображаться в форме('__all__' - будут отображаться все поля, кроме тех, которые заполняются автоматически)
        widgets = { # указываем виджиты для полей
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = { # указываем названия полей, если хотим, чтобы в форме отображалось другое название(label)
            'slug': 'URL'
        }

    def clean_title(self):  # метод для проверки поля title, указываем название поля через_(вместо объявления своего валидатора)
        title = self.cleaned_data['title'] # получаем значение title

        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title


class UploadFileForm(forms.Form):
    # file = forms.FileField(label='Файл') # для загрузка файлов(есть еще ImageField, он заточен для загрузки именно графических изображений(работает с pillow))
    file = forms.ImageField(label='Файл')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='E-mail')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
