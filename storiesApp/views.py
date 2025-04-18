from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import StoryModel
from .serializers import StorySerializer
from .filters import StoryFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class StoryViewSet(viewsets.ModelViewSet):
    queryset = StoryModel.objects.all().order_by('-created_at')
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = StoryFilter

    @action(detail=False, methods=["get"], url_path="active_stories", url_name="active_stories")
    def active_stories(self, request):
        active_stories = self.get_queryset().filter(expires_at__gt=timezone.now())
        serializer = self.get_serializer(active_stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="mark_viewed", url_name="mark_viewed")
    def mark_viewed(self, request, pk=None):
        story = self.get_object()
        user = request.user
        if not story.viewed_by.filter(id=user.id).exists():
            story.viewed_by.add(user)
            story.increment_views()
        serializer = self.get_serializer(story)
        return Response(serializer.data, status=status.HTTP_200_OK)
