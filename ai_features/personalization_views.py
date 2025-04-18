# File: ai_features/personalization_views.py
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import (
    PersonalizationRequestSerializer,
    PersonalizationResponseSerializer,
)

@extend_schema(
    request=PersonalizationRequestSerializer,
    responses=PersonalizationResponseSerializer,
)
class PersonalizationAPIView(GenericAPIView):
    serializer_class = PersonalizationRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recs = generate_personalization(serializer.validated_data['user_id'])
        return Response({'recommendations': recs})


