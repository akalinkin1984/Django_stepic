import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify # можем использовать шаблонные фильтры как функции
from django.views import View
from django.views.generic import TemplateView, ListView

from .models import Women, Category, TagPost, UploadFiles
from .forms import AddPostForm, UploadFileForm

# menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

# data_db = [
#     {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1>
#     (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт
#     (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино,
#     телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
#     Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории,
#     три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''', 'is_published': True},
#     {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
#     {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True}
# ]

# cats_db = [
#     {'id': 1, 'name': 'Актрисы'},
#     {'id': 2, 'name': 'Певицы'},
#     {'id': 3, 'name': 'Спортсменки'},
# ]


# переписали эту функция с помощью класса View
# def index(request):
#     # posts = Women.objects.filter(is_published=1)
#     posts = Women.published.all().select_related('cat')
#
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0
#     }
#     return render(request, 'women/index.html', context=data)


# class WomenHome(TemplateView): # класс для формирования шаблона(переписали метод index с помощью класса унаследованного от TemplateView)
#     template_name = 'women/index.html' # путь к шаблону который будет использоваться
#     extra_context = { # данные которые будут подставлены в шаблон, нельзя получить эти данные из запроса, чтобы получить данные нужно переопределить метод get_context_data
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': Women.published.all().select_related('cat'),
#         'cat_selected': 0
#     }
#
#     # def get_context_data(self, **kwargs): # метод для получения данных из запроса  и формирования переменной для шаблона
#     #     context = super().get_context_data(**kwargs)
#     #     context['title'] = 'Главная страница'
#     #     context['menu'] = menu
#     #     context['posts'] = Women.published.all().select_related('cat')
#     #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
#     #
#     #     return context


class WomenHome(ListView): # переписали класс WomenHome унаследованного от ListView(класс для отображения произвольных списков)
    # model = Women # модель из которой будут браться данные(по-умолчанию берется все записи из указанной таблицы, чтобы выбрать записи нужно прописать метод get_queryset)
    template_name = 'women/index.html' # указываем нужный шаблон
    context_object_name = 'posts' # переменная для отображения статей, через которую обращаемся в шаблоне(по-умолчанию эта переменная - object_list)
    extra_context = { # данные которые будут подставлены в шаблон, нельзя получить эти данные из запроса, чтобы получить данные нужно переопределить метод get_context_data
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0
    }

    def get_queryset(self): # выбираем записи из таблицы
        return Women.published.all().select_related('cat')


# def handle_uploaded_file(f): # функция для загрузки файла
#     name, permission = f.name.split('.')
#     with open(f"uploads/{name}_{uuid.uuid4()}.{permission}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == 'POST':
        # handle_uploaded_file(request.FILES['file_upload']) # сохраняет файл
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file']) # сохраняет файл
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})


# def categories(request, cat_id):
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>id: {cat_id}</p>')
#
#
# def categories_by_slug(request, cat_slug):
#     if request.GET:
#         print(request.GET) # выведем словарь с параметрами GET-запроса
#     if request.POST:
#         print(request.POST) # выведем словарь с параметрами POST-запроса
#     return HttpResponse(f'<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>')
#
#
# def archive(request, year):
#     if year > 2025:
#         # raise Http404 # сработает наш обработчик 404
#
#         # return redirect('/', permanent=True) # перенаправляем на указанный url, в данном случае на главную страницу
#         # # с кодом 302(страница перемещена временно),
#         # #если нужно указать код 301(страница перемещена на постоянный url), указываем permanent=True
#
#         # return redirect(index) # можно указывать функцию-представление(view)
#         # return redirect('cats', 'music')  # можно указывать имя url, РЕКОМЕНДУЕТСЯ делать так, если есть параметры во view, их нужно тоже передавать
#
#         # uri = reverse('cats', args=('music', )) # вычислить uri с помощью reverse, и потом передать его в redirect
#         # return redirect(uri)
#
#         # вместо redirect можно использовать классы HttpResponseRedirect(с кодом 302), HttpResponsePermanentRedirect(с кодом 301)
#         # return HttpResponseRedirect('/') # перенаправление с кодом 302
#
#         uri = reverse('cats', args=('music', )) # вычислить uri, и потом передать его в redirect
#         return HttpResponsePermanentRedirect(uri) # перенаправление с кодом 301
#
#     return HttpResponse(f'<h1>Архив п годам</h1><p>{year}</p>')


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug) # получить 1-у запись из таблицы women по критерию pk=post_idб если запись не найдена генерирует 404
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1
    }

    return render(request, 'women/post.html', data)


# переписали эту функция с помощью класса View
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#
#             # # если форма не связана с моделью
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#
#             # если форма связана с моделью
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#
#     }
#     return render(request, 'women/addpage.html', data)


class AddPage(View): # переписали метод addpage с помощью класса унаследованного от View
    def get(self, request):
        form = AddPostForm()
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form

        }
        return render(request, 'women/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form

        }
        return render(request, 'women/addpage.html', data)


def contact(request):
    return HttpResponse(f'Обратная связь')


def login(request):
    return HttpResponse(f'Авторизация')


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related('cat')
#
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk
#     }
#     return render(request, 'women/index.html', context=data)


class WomenCategory(ListView): # с помощью класс переписали функцию show_category унаследованного от ListView(класс для отображения произвольных списков)
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False # если записи не находятся(список posts пустой), то будет генерироваться исключение 404(запрещается показывать пустые списки)

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs): # метод для получения данных из запроса и формирования переменной для шаблона
            context = super().get_context_data(**kwargs)
            cat = context['posts'][0].cat
            context['title'] = 'Категория - ' + cat.name
            context['menu'] = menu
            context['cat_selected'] = cat.pk

            return context


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None
#     }
#     return render(request, 'women/index.html', context=data)


class TagList(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тег - ' + self.kwargs['tag_slug']
        context['menu'] = menu

        return context


def page_not_found(request, exception): # обработчик 404, если DEBUG = False и в ALLOWED_HOSTS добавлен разрешенный хост(127.0.0.1)
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
