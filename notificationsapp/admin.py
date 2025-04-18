from django.contrib import admin
from .models import NotificationModel

@admin.register(NotificationModel)
class NotificationModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')
    list_filter = ('is_read', 'created_at')
