# File: usersapp/apps.py
from django.apps import AppConfig

class UsersappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usersapp'

    def ready(self):
        # Delay model imports until all apps are loaded.
        from django.contrib.auth.models import User
        # You can add additional startup logic or signal registration here.
