from django.contrib import admin
from .models import ChatRoomModel, ChatHistoryModel

admin.site.register(ChatRoomModel)
admin.site.register(ChatHistoryModel)
