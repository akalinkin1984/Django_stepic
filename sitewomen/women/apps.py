from django.apps import AppConfig


class WomenConfig(AppConfig):
    verbose_name = 'Женщины мира' # определяет название приложения в админ панели
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
