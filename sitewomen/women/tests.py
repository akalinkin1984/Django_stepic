from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Women


class GetPagesTestCase(TestCase):
    fixtures = ['women_women.json', 'women_category.json', 'women_husband.json', 'women_tagpost.json']  # фикстуры которые будут загружаться в тестовую БД перед каждым тестом(по-умолчанию создается пустая тестовая БД)

    def setUp(self):
        """Инициализация перед выполнением каждого теста"""
        pass

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)  # получить ответ от сервера(имитируем обращение к главной странице)
        # self.assertEqual(response.status_code, 200)  # проверяет на равенство 2-х переданных аргументов
        self.assertEqual(response.status_code, HTTPStatus.OK)  # заменили число 200 на HTTPStatus.OK
        self.assertIn('women/index.html', response.template_name)  # проверяет вхождение первого аргумента во второй(проверим что используется нужный шаблон)
        self.assertTemplateUsed(response, 'women/index.html')  # проверяет что используется указанный шаблон
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):  # проверка на redirect страницы addpage
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # HTTPStatus.FOUND - перенаправление(код 302)
        self.assertRedirects(response, redirect_uri)  # проверяет перенаправление(аргументы - объект response, маршрут на который должны перейти)

    def test_data_mainpage(self):
        w = Women.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], w[:3])  # проверка на равенство кверисетов, проверяем первые 3 элемента, т.к. настроена пагинация по 3 записи на странице

    def test_paginate_mainpage(self):  # тест на пагинацию
        path = reverse('home')
        page = 2  # текущая страница которая будет отображаться
        paginate_by = 3  # кол-во записей на странице
        response = self.client.get(path + f'?page={page}')
        w = Women.published.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['posts'], w[(page - 1) * paginate_by:page * paginate_by])

    def test_content_post(self):  # проверка отображения содержимого поста
        w = Women.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)

    def tearDown(self):
        """Действия после выполнения каждого теста"""
        pass


# python manage.py test . - в текущем проекте будет выполнен поиск всех тестов во всех приложениях и последовательно запущены
# python manage.py test women - запустить тесты строго определенного приложения
# python manage.py test women.tests.GetPagesTestCase - можно отдельно указать класс (группу) тестов
# python manage.py test women.tests.GetPagesTestCase.test_case_1 - запуск отдельного теста

# Для формирования фикстур
# python -Xutf8 manage.py dumpdata women.women -o women/fixtures/women_women.json
# python -Xutf8 manage.py dumpdata women.category -o women/fixtures/women_category.json
# python -Xutf8 manage.py dumpdata women.husband -o women/fixtures/women_husband.json
# python -Xutf8 manage.py dumpdata women.tagpost -o women/fixtures/women_tagpost.json
