from django.contrib import admin
from .models import DashboardLog

@admin.register(DashboardLog)
class DashboardLogAdmin(admin.ModelAdmin):
    list_display = [
        'timestamp', 'company', 'shop',
        'total_bookings', 'total_revenue', 'total_specialists',
        'total_stories', 'total_story_likes', 'total_reels'
    ]
    list_filter = ['company', 'shop', 'timestamp']
    search_fields = ['company__name', 'shop__shop_name']
