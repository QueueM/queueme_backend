from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (CustomerReportApiView,ShopReportApiView, ServiceReportApiView, ServiceBookingReportApiView,
                    EmployeeReportApiView, MarketingReportApiView, ReelsReportApiVIew, ChatReportApiView)

# Initialize the router
router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("customer-report/", CustomerReportApiView.as_view(), name="customer_report"),
    path("shop-report/", ShopReportApiView.as_view(), name="shop_report"),
    path("service-report/", ServiceReportApiView.as_view(), name="service_report"),
    path("booking-service-report/", ServiceBookingReportApiView.as_view(),
         name="booking_service_report"),
    path("employee-report/", EmployeeReportApiView.as_view(), name="employee_report"),
    path("market-report/", MarketingReportApiView.as_view(), name="market_report"),
    path("reels-report/", ReelsReportApiVIew.as_view(), name="reels_report"),
    path("chat-report/", ChatReportApiView.as_view(), name="chat_report")
]
