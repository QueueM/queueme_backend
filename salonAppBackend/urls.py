# File: salonAppBackend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from payment.webhook import WebHookApiView

# drf-spectacular schema views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def api_overview(request):
    return JsonResponse({
        "message": "Welcome to QueueMe API 🚀",
        "endpoints": {
            "Auth": {
                "Get OTP": "/auth/get-otp/",
                "Register": "/auth/register/",
                "Login With OTP": "/auth/get-token-with-otp/",
                "Token": "/auth/api/token/",
                "Token Refresh": "/auth/api/token/refresh/",
                "Logout": "/auth/logout/"
            },
            "Users": "/users/",
            "Company": "/company/",
            "Customers": "/customers/",
            "Shops": "/shops/",
            "Reviews": "/reviews/",
            "Reels": "/reels/",
            "Stories": "/stories/",
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
    # OpenAPI schema (JSON)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI (optional)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API overview
    path('', api_overview, name='api_overview'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Auth
    path('auth/', include('authapp.urls')),

    # Core API routes
    path('users/', include('usersapp.urls')),
    path('api/ai/', include('ai_features.urls')),
    path('dashboard/', include('shopDashboardApp.urls')),
    path('reviews/', include('reviewapp.urls')),
    path('company/', include('companyApp.urls')),
    path('customers/', include('customersApp.urls')),
    path('shops/', include('shopApp.urls')),
    path('follow/', include('followApp.urls')),
    path('reels/', include('reelsApp.urls')),
    path('stories/', include(('storiesApp.urls', 'storiesApp'), namespace='storiesApp')),
    path('employees/', include('employeeApp.urls')),
    path('notifications/', include('notificationsapp.urls')),
    path('subscriptions/', include('subscriptionApp.urls')),
    path('payment/', include('payment.urls')),
    path('ads/', include('adsApp.urls')),
    path('chat/', include('chatApp.urls')),
    path('shop-service/', include(('shopServiceApp.urls', 'shopServiceApp'), namespace='shopServiceApp')),

    # Payment webhook
    path('payment/webhook/', WebHookApiView.as_view(), name="payment_callback"),
]
