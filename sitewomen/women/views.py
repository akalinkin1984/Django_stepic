from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify # можем использовать шаблонные фильтры как функции


menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True}
]


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db
    }
    return render(request, 'women/index.html', context=data)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте'})


def categories(request, cat_id):
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>id: {cat_id}</p>')


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET) # выведем словарь с параметрами GET-запроса
    if request.POST:
        print(request.POST) # выведем словарь с параметрами POST-запроса
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>')


def archive(request, year):
    if year > 2025:
        # raise Http404 # сработает наш обработчик 404

        # return redirect('/', permanent=True) # перенаправляем на указанный url, в данном случае на главную страницу
        # # с кодом 302(страница перемещена временно),
        # #если нужно указать код 301(страница перемещена на постоянный url), указываем permanent=True

        # return redirect(index) # можно указывать функцию-представление(view)
        # return redirect('cats', 'music')  # можно указывать имя url, РЕКОМЕНДУЕТСЯ делать так, если есть параметры во view, их нужно тоже передавать

        # uri = reverse('cats', args=('music', )) # вычислить uri с помощью reverse, и потом передать его в redirect
        # return redirect(uri)

        # вместо redirect можно использовать классы HttpResponseRedirect(с кодом 302), HttpResponsePermanentRedirect(с кодом 301)
        # return HttpResponseRedirect('/') # перенаправление с кодом 302

        uri = reverse('cats', args=('music', )) # вычислить uri, и потом передать его в redirect
        return HttpResponsePermanentRedirect(uri) # перенаправление с кодом 301

    return HttpResponse(f'<h1>Архив п годам</h1><p>{year}</p>')


def page_not_found(request, exception): # обработчик 404, если DEBUG = False и в ALLOWED_HOSTS добавлен разрешенный хост(127.0.0.1)
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
