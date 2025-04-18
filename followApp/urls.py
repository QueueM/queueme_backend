# followApp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopFollowViewSet, FeedView

router = DefaultRouter()
router.register(r'follows', ShopFollowViewSet, basename='follows')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='follow-feed'),
]
