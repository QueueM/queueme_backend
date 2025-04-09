from django.apps import AppConfig


class ShopServiceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopServiceApp'

    def ready(self):
        # Register signal handlers
        import shopServiceApp.signals  # noqa: F401
