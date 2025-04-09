from django.apps import AppConfig

class CompanyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'companyApp'

    def ready(self):
        # Register AI-related signal handlers
        import companyApp.signals
