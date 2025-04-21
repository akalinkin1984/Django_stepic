from django import template

import women.views as views


register = template.Library()


@register.simple_tag(name='getcats') # регистрируем свой тег как простой тег(возвращает данные), и указываем имя тега
def get_categories(): # создаем свой тег в виде функции
    return views.cats_db


@register.inclusion_tag('women/list_categories.html') # регистрируем свой тег как включающий тег(возвращает фрагмент html страницы) и указываем путь к шаблону который возвратится
def show_categories(cat_selected=0):
    cats = views.cats_db
    return {'cats': cats, 'cat_selected': cat_selected}
