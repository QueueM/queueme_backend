from django.apps import AppConfig

class ShopappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopApp'

    def ready(self):
        # Import signals to ensure they are registered on app startup.
        import shopApp.signals  # noqa: F401
