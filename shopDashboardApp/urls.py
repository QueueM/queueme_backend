from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DashboardLogViewSet

router = DefaultRouter()
router.register(r'dashboard-logs', DashboardLogViewSet, basename='dashboard-log')

urlpatterns = [
    path('', include(router.urls)),
]
