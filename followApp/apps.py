# followApp/apps.py
from django.apps import AppConfig

class FollowAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'followApp'

    def ready(self):
        # This can be used to import signals if needed.
        pass
