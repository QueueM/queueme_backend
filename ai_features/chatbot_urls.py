from django.urls import path
from .chatbot_views import ChatbotAPIView

urlpatterns = [
    path('', ChatbotAPIView.as_view(), name='chatbot'),
]
