from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReelsViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'reels', ReelsViewSet, basename='reels')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]
