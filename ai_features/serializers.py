# File: ai_features/serializers.py
from rest_framework import serializers

# --- Churn Prediction ---
class ChurnPredictionRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    history = serializers.JSONField()

class ChurnPredictionResponseSerializer(serializers.Serializer):
    will_churn = serializers.BooleanField()
    score = serializers.FloatField()


# --- Customer Segmentation ---
class CustomerSegmentationRequestSerializer(serializers.Serializer):
    shop_id = serializers.IntegerField()

class CustomerSegmentationResponseSerializer(serializers.Serializer):
    segments = serializers.ListField(child=serializers.DictField())


# --- Employee Performance ---
class EmployeePerformanceRequestSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    period = serializers.CharField()

class EmployeePerformanceResponseSerializer(serializers.Serializer):
    performance_score = serializers.FloatField()
    metrics = serializers.DictField(child=serializers.FloatField())


# --- Forecasting ---
class ForecastingRequestSerializer(serializers.Serializer):
    shop_id = serializers.IntegerField()
    horizon = serializers.IntegerField()

class ForecastingResponseSerializer(serializers.Serializer):
    forecast = serializers.ListField(child=serializers.DictField())


# --- Fraud Detection ---
class FraudDetectionRequestSerializer(serializers.Serializer):
    transaction_id = serializers.CharField()
    amount = serializers.FloatField()

class FraudDetectionResponseSerializer(serializers.Serializer):
    is_fraud = serializers.BooleanField()
    probability = serializers.FloatField()


# --- Image Analysis ---
class ImageAnalysisRequestSerializer(serializers.Serializer):
    image_url = serializers.URLField()

class ImageAnalysisResponseSerializer(serializers.Serializer):
    analysis = serializers.JSONField()


# --- Personalization ---
class PersonalizationRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class PersonalizationResponseSerializer(serializers.Serializer):
    recommendations = serializers.ListField(child=serializers.DictField())


# --- Recommendation (Marketing) ---
class RecommendationResponseSerializer(serializers.Serializer):
    recommendations = serializers.ListField(child=serializers.DictField())


# --- Sentiment Analysis ---
class SentimentRequestSerializer(serializers.Serializer):
    text = serializers.CharField()

class SentimentResponseSerializer(serializers.Serializer):
    sentiment = serializers.ChoiceField(choices=[('positive','Positive'),
                                                ('neutral','Neutral'),
                                                ('negative','Negative')])
    score = serializers.FloatField()
