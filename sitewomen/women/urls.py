from django.urls import path, re_path, register_converter
from django.views.decorators.cache import cache_page  # для кэширования отдельных страниц сайта

from . import views, converters


register_converter(converters.FourDigitYearConverter, 'year4') # регистрируем конвертер

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.WomenHome.as_view(), name='home'),  # в as_view можно передавать словарь с данными для формирования шаблона через параметр extra_context, данные будут браться отсюда, а не из функции представления
    # path('', cache_page(30)(views.WomenHome.as_view()), name='home'),  # с использование кэша
    path('about/', views.about, name='about'),
    # path('addpage/', views.addpage, name='add_page'),
    path('addpage/', views.AddPage.as_view(), name='add_page'), # регестрируем класс с помощью метода as_view()
    # path('contact/', views.contact, name='contact'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('login/', views.login, name='login'),
    # path('post/<int:post_id>/', views.show_post, name='post'),
    # path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    # path('category/<int:cat_id>/', views.show_category, name='category'),
    # path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    # path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    # path('cats/<int:cat_id>/', views.categories, name='cats_id'), # рекомендуется использовать name, для обращения к url в программе
    # path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    # # re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive), # использование регулярных выражений в пути
    # path('archive/<year4:year>/', views.archive, name='archive'), # используем свой конвертер
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='update'),
    path('delete/<slug:slug>/', views.DeletePage.as_view(), name='delete'),
]
