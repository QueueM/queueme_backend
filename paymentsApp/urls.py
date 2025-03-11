from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, MoyasarWebhookView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhook/moyasar/', MoyasarWebhookView.as_view(), name='moyasar-webhook')
]
