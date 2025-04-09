# reelsApp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReelsViewSet, CommentViewSet, StoryViewSet

router = DefaultRouter()
router.register(r'reels', ReelsViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'stories', StoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
