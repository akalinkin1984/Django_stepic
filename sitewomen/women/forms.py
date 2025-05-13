from django import forms
from .models import Category, Husband


class AddPostForm(forms.Form): # определяем класс для отображения формы не связанной с моделью
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False) # многострочный текст, required - необязательное поле
    is_published = forms.BooleanField(required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all()) # выпадающий список
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False) # выпадающий список
