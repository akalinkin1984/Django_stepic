from django.db import models
from django.urls import reverse


# Create your models here.
class PublishedManager(models.Manager): # определяем класс своего менеджера модели
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager() # указываем менеджер objects, иначе он перестанет работать после определения своего менеджера
    published = PublishedManager() # определяем свой менеджер

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_create'] # задать сортировку по-умолчанию(- означает в обратном порядке)
        indexes = [
            models.Index(fields=['-time_create']) # проиндексировать поле time_create с учетом сортировки(-)
        ]

    def get_absolute_url(self): # возвращает url каждой записи таблицы
        return reverse('post', kwargs={'post_slug': self.slug})
