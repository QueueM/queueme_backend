



from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EmployeeDetailsViewset
router = DefaultRouter()
router.register(r'employees', EmployeeDetailsViewset)


urlpatterns = [
    path('', include(router.urls)),
]
