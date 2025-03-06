from django.contrib import admin

# Register your models here.

from .models import ChatRoomModel, ChatHistoryModel

admin.site.register(ChatRoomModel)
admin.site.register(ChatHistoryModel)