# File: ai_features/personalization_urls.py
from django.urls import path
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ai_features.serializers import (
    PersonalizationRequestSerializer,
    PersonalizationResponseSerializer,
)
from ai_features.personalization import generate_personalization

@extend_schema(
    request=PersonalizationRequestSerializer,
    responses=PersonalizationResponseSerializer,
)
class PersonalizationAPIView(GenericAPIView):
    serializer_class = PersonalizationRequestSerializer

    def post(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)
        recs = generate_personalization(data.validated_data['user_id'])
        return Response({'recommendations': recs})

urlpatterns = [
    path('', PersonalizationAPIView.as_view(), name='personalization'),
]
