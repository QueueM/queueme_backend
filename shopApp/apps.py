# shopApp/apps.py
from django.apps import AppConfig

class ShopappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopApp'

    def ready(self):
        # Import signals so that they are registered.
        import shopApp.signals
