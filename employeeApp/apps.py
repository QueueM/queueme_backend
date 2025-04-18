from django.apps import AppConfig

class EmployeeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employeeApp'

    def ready(self):
        import employeeApp.signals  # noqa: F401
