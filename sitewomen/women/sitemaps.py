from django.contrib.sitemaps import Sitemap

from .models import Women, Category


class PostSitemap(Sitemap):  # класс для формирования данных карты сайта(будет отдавать все посты с главной страницы)
    changefreq = 'monthly'  # частота обновления страниц(ежемесячно)
    priority = 0.9  # приоритет

    def items(self):  # метод возвращает записи которые попадут в карту сайта
        return Women.published.all()

    def lastmod(self, obj):  # метод возвращает время последнего изменения страницы
        return obj.time_update


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Category.objects.all()
