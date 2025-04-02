from  rest_framework.routers import DefaultRouter 
from django.urls import path, include
from .views import(ShopReportApiView ,ServiceReportApiView)

# Initialize the router
router = DefaultRouter()

# # Register the viewset with the router
# router.register("customer", CustomersReportApiViewSet, basename="customer_report")
  


urlpatterns = [
    path("", include(router.urls)) ,
    path("shop-report/", ShopReportApiView.as_view(), name="shop_report"),
    path("service-report/",ServiceReportApiView.as_view(), name="service_report")
]
