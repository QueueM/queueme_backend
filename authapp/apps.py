from django.apps import AppConfig

class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'

    def ready(self):
        # Import signals so that login risk analysis fires on authentication events.
        import authapp.signals  # noqa: F401
