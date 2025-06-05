"""
URL configuration for sitewomen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib.sitemaps.views import sitemap  # для карты сайта
from django.views.decorators.cache import cache_page

from sitewomen import settings
from women import views
from women.sitemaps import PostSitemap, CategorySitemap

sitemaps = {  # словарь который будем передавать в функцию sitemap
    'posts': PostSitemap,
    'cats': CategorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index),
    # path('cats/', views.categories),
    path('', include('women.urls')), # подключение путей из файла women.urls
    path('users/', include('users.urls', namespace='users')), # подключение путей из файла users.urls(namespace - пространство имен, напр. чтобы обратиться к маршруту login, пишем "users:login")
    path("social-auth/", include('social_django.urls', namespace="social")),
    path("captcha/", include('captcha.urls')),
    path("sitemap.xml", cache_page(86400)(sitemap), {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),  # путь для карты сайта
] + debug_toolbar_urls()

if settings.DEBUG: # добавляем маршрут который связывает префикс MEDIA_URL с маршрутом MEDIA_ROOT, для отображения фото в режиме DEBUG
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found # переопределяем обработчик 404 на свой, если DEBUG = False и в ALLOWED_HOSTS добавлен разрешенный хост(127.0.0.1)
# Аналогичным образом можно переопределять обработчики других исключений, например:
#
# handler500 – ошибка сервера
# handler403 – доступ запрещен
# handler400 – невозможно обработать запрос

admin.site.site_header = 'Панель администрирования' # определяет общее название админ-панели
admin.site.index_title = 'Известные женщины мира' # определяет уточненное название админ-панели (подзаголовок)
