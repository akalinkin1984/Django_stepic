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
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

from women import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.index),
    # path('cats/', views.categories),
    path('', include('women.urls')) # подключение путей из файла women.urls
] + debug_toolbar_urls()

handler404 = views.page_not_found # переопределяем обработчик 404 на свой, если DEBUG = False и в ALLOWED_HOSTS добавлен разрешенный хост(127.0.0.1)
# Аналогичным образом можно переопределять обработчики других исключений, например:
#
# handler500 – ошибка сервера
# handler403 – доступ запрещен
# handler400 – невозможно обработать запрос
