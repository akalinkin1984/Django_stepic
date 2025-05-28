from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from . import views


app_name = 'users' # нужно прописать, если используем namespace в основном файле urls(такое же имя)

urlpatterns = [
    # path('login/', views.login_user, name='login'),
    path('login/', views.LoginUser.as_view(), name='login'),
    # path('logout/', views.logout_user, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('register/', views.register, name='register'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'), # для редактирования пароля
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'), # для отображения при успешном редактировании пароля
]
