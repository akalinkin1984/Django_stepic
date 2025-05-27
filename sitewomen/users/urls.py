from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


app_name = 'users' # нужно прописать, если используем namespace в основном файле urls(такое же имя)

urlpatterns = [
    # path('login/', views.login_user, name='login'),
    path('login/', views.LoginUser.as_view(), name='login'),
    # path('logout/', views.logout_user, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
