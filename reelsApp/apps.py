from django.apps import AppConfig

class ReelsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reelsApp'

    def ready(self):
        import reelsApp.signals  # noqa: F401
