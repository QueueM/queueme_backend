# companyApp/apps.py
from django.apps import AppConfig

class CompanyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'companyApp'

    def ready(self):
        # Import signals to register them on app startup.
        import companyApp.signals
