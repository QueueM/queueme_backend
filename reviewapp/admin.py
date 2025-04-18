from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'rating', 'sentiment_score', 'content_object', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'title', 'comment')
