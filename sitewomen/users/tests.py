from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user_1',
            'email': 'user1@sitewomen.ru',
            'first_name': 'Sergey',
            'last_name': 'Balakirev',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }

    def test_form_registration_get(self):
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_success(self):  # тест на регистрацию пользователя
        user_model = get_user_model()
        path = reverse('users:register')
        response = self.client.post(path, self.data)  # post запрос с передачей данных

        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # проверяем что было перенаправление
        self.assertRedirects(response, reverse('users:login'))  # проверяем что перенаправление было на нужную страницу
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())  # проверяем что пользователь был занесен в БД

    def test_user_registration_password_error(self):  # тест ошибки при вводе неправильного пароля
        self.data['password2'] = '12345678A'

        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введенные пароли не совпадают.', html=True)  # проверяем что строка содержится на странице(html=True - проверяет на полное соответсвие строки c html тегом)

    def test_user_registration_exists_error(self):  # тест на то что 2 пользователя с одинаковым логином создавать нельзя
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'])
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует')
