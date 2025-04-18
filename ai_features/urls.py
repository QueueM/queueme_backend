# File: ai_features/urls.py
from django.urls import path, include

urlpatterns = [
    path('churn/', include('ai_features.churn_prediction_urls')),
    path('segmentation/', include('ai_features.customer_segmentation_urls')),
    path('employee-performance/', include('ai_features.employee_performance_urls')),
    path('forecasting/', include('ai_features.forecasting_urls')),
    path('fraud/', include('ai_features.fraud_detection_urls')),
    path('image-analysis/', include('ai_features.image_analysis_urls')),
    path('personalization/', include('ai_features.personalization_urls')),
    path('recommendations/', include('ai_features.recommendation_urls')),
    path('sentiment/', include('ai_features.sentiment_urls')),
]
