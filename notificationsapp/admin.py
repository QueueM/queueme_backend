from django.contrib import admin

# Register your models here.


from .models import NotificationModel

admin.site.register(NotificationModel)