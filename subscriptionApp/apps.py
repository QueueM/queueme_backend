from django.apps import AppConfig

class SubscriptionappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscriptionApp'

    def ready(self):
        import subscriptionApp.signals  # noqa: F401
