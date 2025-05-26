from django.urls import path
from . import views


app_name = 'users' # нужно прописать, если используем namespace в основном файле urls(такое же имя)

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]