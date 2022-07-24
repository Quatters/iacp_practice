from django.apps import AppConfig as DefaultAppConfig
from django.utils.translation import gettext_lazy


class AppConfig(DefaultAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = gettext_lazy('site')
