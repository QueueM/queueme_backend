from django.apps import AppConfig

class CompanyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'companyApp'

    def ready(self):
        # Import signals to register AI forecast and fraud detection updates.
        import companyApp.signals
