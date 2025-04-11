# shopApp/apps.py
from django.apps import AppConfig

class ShopappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopApp'

    def ready(self):
        # Import signals to register them on app startup.
        import shopApp.signals
