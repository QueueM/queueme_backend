from django.apps import AppConfig

class StoriesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storiesApp'

    def ready(self):
        import storiesApp.signals  # noqa: F401
