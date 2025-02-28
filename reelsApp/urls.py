

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReelsViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'reels', ReelsViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('register/', RegisterAsCompanyAPIView.as_view())
    
]
