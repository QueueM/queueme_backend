from django.apps import AppConfig

class AdsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adsApp'

    def ready(self):
        import adsApp.signals  # noqa: F401
