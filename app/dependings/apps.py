from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DependingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dependings'
    verbose_name = _('НАСТРОЙКА ЗАВИСИМОСТЕЙ')
