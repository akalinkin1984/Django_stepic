from django.contrib import admin, messages
from .models import Women, Category


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin): # класс для регистрации и отображения записей таблицы women в админ панели
    list_display = ['title', 'time_create', 'is_published', 'cat', 'brief_women'] # какие поля отображать
    list_display_links = ['title'] # какие поля можно кликать
    ordering = ['time_create', 'title'] # по каким полям происходит сортировка в админ панели
    list_editable = ['is_published'] # какие поля можно изменять с главной страницы
    list_per_page = 5 # количество записей на странице(пагинация) в админ панели
    actions = ['set_published', 'set_draft'] # добавляем свои пункты в меню 'действие'

    @admin.display(description='Краткое описание', ordering='content')  # декоратор для отображения названия поля в админ панели и сортировкой данного поля по полю content
    def brief_women(self, women: Women): # этот метод можем использовать в list_display для отображения еще одного поля
        return f'Описание {len(women.content)} символов' # возвращает кол-во символов в описании

    @admin.action(description='Опубликовать выбранные записи') # декоратор для отображения названия метода
    def set_published(self, request, queryset): # метод для добавления действия для выбранных записей
        count = queryset.update(is_published=Women.Status.PUBLISHED) # устанавливаем статус в 'опубликовано'
        self.message_user(request, f'Изменено {count} записей') # для отображения сообщения сколько записей изменено

    @admin.action(description='Снять с публикации выбранные записи')  # декоратор для отображения названия метода
    def set_draft(self, request, queryset):  # метод для добавления действия для выбранных записей
        count = queryset.update(is_published=Women.Status.DRAFT)  # устанавливаем статус в 'черновик'
        self.message_user(request, f'{count} записей снято с публикации', messages.WARNING)  # для отображения сообщения сколько записей изменено с типом WARNING


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


# admin.site.register(Women, WomenAdmin) # регистрируем данным способом без использования декоратора
