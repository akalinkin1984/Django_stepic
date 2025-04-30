from django import template
from django.db.models import Count

import women.views as views
from women.models import Category, TagPost

register = template.Library()


# @register.simple_tag(name='getcats') # регистрируем свой тег как простой тег(возвращает данные), и указываем имя тега
# def get_categories(): # создаем свой тег в виде функции
#     return views.cats_db


@register.inclusion_tag('women/list_categories.html') # регистрируем свой тег как включающий тег(возвращает фрагмент html страницы) и указываем путь к шаблону который возвратится
def show_categories(cat_selected=0):
    # cats = views.cats_db
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/list_tags.html') # регистрируем свой тег как включающий тег(возвращает фрагмент html страницы) и указываем путь к шаблону который возвратится
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
