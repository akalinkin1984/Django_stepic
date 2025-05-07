from django.contrib import admin, messages
from .models import Women, Category


class MarriedFilter(admin.SimpleListFilter): # создаем свой фильтр(замужем или нет)
    title = 'Статус женщин' # название фильтра
    parameter_name = 'status' # такое название параметра будет в запросе(url)

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'), # значение параметра status в запросе(url) и название в панели фильтра
            ('single', 'Не замужем') # значение параметра status в запросе(url) и название в панели фильтра
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married': # возвращает значение параметра status
            return queryset.filter(husband__isnull=False)
        if self.value() == 'single': # возвращает значение параметра status
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin): # класс для регистрации и отображения записей таблицы women в админ панели
    fields = ['title', 'slug', 'content', 'cat', 'husband', 'tags'] # поля которые будут отображаться в форме редактирования(создания) записи
    # exclude = ['tags', 'is_published'] # поля которые НЕ будут отображаться в форме редактирования(создания) записи
    # readonly_fields = ['slug'] # поля только для чтения
    prepopulated_fields = {'slug': ('title', )} # указываем на основе чего формируется слаг автоматически, слаг обязательно должен быть разрещен для записи
    # filter_horizontal = ['tags'] # фильтр для связи многие ко многим
    filter_vertical = ['tags']  # фильтр для связи многие ко многим
    list_display = ['title', 'time_create', 'is_published', 'cat', 'brief_women'] # какие поля отображать
    list_display_links = ['title'] # какие поля можно кликать
    ordering = ['time_create', 'title'] # по каким полям происходит сортировка в админ панели
    list_editable = ['is_published'] # какие поля можно редактировать с главной страницы
    list_per_page = 5 # количество записей на странице(пагинация) в админ панели
    actions = ['set_published', 'set_draft'] # добавляем свои пункты в меню 'действие'
    search_fields = ['title__startswith', 'cat__name'] # список полей по которым осуществляется поиск(если не указать этот пункт, поиска не будет вообще)
    list_filter = [MarriedFilter, 'cat__name', 'is_published'] # поля по которым будет производиться фильтрация(если не указать этот пункт, фильтра не будет вообще)

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
