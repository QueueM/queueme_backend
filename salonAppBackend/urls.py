"""
URL configuration for salonAppBackend project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from helpers.payment.webhook import WebHookApiView

# Define a root API overview view
def api_overview(request):
    return JsonResponse({
        "message": "Welcome to QueueMe API 🚀",
        "endpoints": {
            "Auth": {
                "Get OTP": "/auth/get-otp/",
                "Register": "/auth/register/",
                "Login With OTP": "/auth/get-token-with-otp/",
                "Token": "/auth/api/token/",
                "Token Refresh": "/auth/api/token/refresh/"
            },
            "Users": "/users/",
            "Company": "/company/",
            "Customers": "/customers/",
            "Shops": "/shops/",
            "Reviews": "/api/",
            "Reels": "/reels/",
            
            "Employees": "/employees/",
            "Notifications": "/notifications/",
            "Subscriptions": "/subscriptions/",
            "Ads": "/ads/",
            "Chat": "/chat/",
            "AI": {
                "Recommendations": "/api/ai/recommendations/",
                "Sentiment": "/api/ai/sentiment/",
                "Chatbot": "/api/ai/chatbot/",
                "Forecast": "/api/ai/forecast/",
                "Fraud Detection": "/api/ai/fraud/",
                "Personalization": "/api/ai/personalization/",
                "Image Analysis": "/api/ai/image-analysis/"
            },
            "Payment Webhook": "/payment/webhook/"
        }
    })

urlpatterns = [
    path('', api_overview),  # Root overview endpoint
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls')),
    path('users/', include('usersapp.urls')),
    path('api/ai/', include('ai_features.urls')),
    # salonAppBackend/urls.py or wherever you include apps
    path('dashboard/', include('shopDashboardApp.urls')),
    path('reviews/', include('reviewapp.urls')),
    path('company/', include('companyApp.urls')),
    path('customers/', include('customersApp.urls')),
    path('shops/', include('shopApp.urls')),
    path('api/', include('reviewapp.urls')),
    path('reels/', include('reelsApp.urls')),
    path('employees/', include('employeeApp.urls')),
    path('notifications/', include('notificationsapp.urls')),
    path('subscriptions/', include('subscriptionApp.urls')),
    path('ads/', include('adsApp.urls')),
    path('chat/', include('chatApp.urls')),
    path('payment/webhook/', WebHookApiView.as_view(), name="payment_callback"),
]
