from django.urls import path, include

urlpatterns = [
    path('recommendations/', include('ai_features.recommendation_urls')),
    path('sentiment/', include('ai_features.sentiment_urls')),
    path('chatbot/', include('ai_features.chatbot_urls')),
    path('forecast/', include('ai_features.forecasting_urls')),
    path('fraud/', include('ai_features.fraud_detection_urls')),
    path('personalization/', include('ai_features.personalization_urls')),
    path('image-analysis/', include('ai_features.image_analysis_urls')),
]
