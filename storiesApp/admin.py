from django.contrib import admin
from .models import StoryModel, StoryViewedModel

@admin.register(StoryModel)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'created_at', 'expires_at', 'view_count')
    list_filter = ('created_at',)
    search_fields = ('shop__shop_name', 'caption')
    readonly_fields = ('view_count', 'created_at', 'expires_at', 'ai_video_tags', 'analytics_data')

@admin.register(StoryViewedModel)
class StoryViewedAdmin(admin.ModelAdmin):
    list_display = ('id', 'story', 'user', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('story__id', 'user__username')
