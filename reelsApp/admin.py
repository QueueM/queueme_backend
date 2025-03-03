from django.contrib import admin

# Register your models here.

from .models import ReelsModel, CommentsModel, StoryModel

admin.site.register(ReelsModel)
admin.site.register(CommentsModel)
admin.site.register(StoryModel)