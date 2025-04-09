# authApp/apps.py
from django.apps import AppConfig

class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'

    def ready(self):
        # Import the signals using the correct module name (lowercase)
        import authapp.signals  # noqa: F401
