from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


def translit_to_eng(s: str) -> str: # функция для определения слага для русских букв
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ë': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 'c', 'т': 't', 'у': 'u', 'ф': 'f', 'x': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 's': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))
class PublishedManager(models.Manager): # определяем класс своего менеджера модели
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок') # verbose_name для отображения а админ панели(но не только)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                                     default=Status.DRAFT, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='woman', verbose_name='Муж')

    objects = models.Manager() # указываем менеджер objects, иначе он перестанет работать после определения своего менеджера
    published = PublishedManager() # определяем свой менеджер

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Известные женщины' # определяет названия модели в единств. числе в админ панели
        verbose_name_plural = 'Известные женщины' # определяет названия модели во множеств. числе в админ панели
        ordering = ['-time_create'] # задать сортировку по-умолчанию(- означает в обратном порядке)
        indexes = [
            models.Index(fields=['-time_create']) # проиндексировать поле time_create с учетом сортировки(-)
        ]

    def get_absolute_url(self): # возвращает url каждой записи таблицы, так же определяет наличие кнопки смотреть на сайте в админ панели
        return reverse('post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs): # (вариант 1)метод для автоматического формирования слага(работает только с англ. буквами, для русских букв используем свою функцию)
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self): # возвращает url каждой записи таблицы
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name
