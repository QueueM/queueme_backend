# reelsApp/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ReelsModel, CommentsModel, StoryModel
from .serializers import ReelSerializer, CommentSerializer, StorySerializer
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ReelsFilter, ReelsCommentsFilter, StoryFilter
from rest_framework.permissions import IsAuthenticated

class ReelsViewSet(CustomBaseModelViewSet):
    queryset = ReelsModel.objects.all().order_by('-created_at')
    serializer_class = ReelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReelsFilter
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        reel = self.get_object()
        if request.user in reel.likes.all():
            reel.likes.remove(request.user)
        else:
            reel.likes.add(request.user)
        serializer = ReelSerializer(reel, context={'user': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentViewSet(CustomBaseModelViewSet):
    queryset = CommentsModel.objects.filter(parent=None).order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReelsCommentsFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['POST'])
    def reply(self, request, pk=None):
        parent_comment = self.get_object()
        text = request.data.get('text')
        if not text:
            return Response({"message": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)
        reply = CommentsModel.objects.create(user=request.user, reel=parent_comment.reel, text=text, parent=parent_comment)
        return Response(CommentSerializer(reply, context={'user': request.user}).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        comment = self.get_object()
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        serializer = CommentSerializer(comment, context={'user': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)

class StoryViewSet(CustomBaseModelViewSet):
    queryset = StoryModel.objects.order_by('-created_at')
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = StoryFilter
    
    @action(detail=False, methods=["get"], url_path="get-stories-list", url_name="get-stories-list")
    def get_stories_list(self, request, *args, **kwargs):
        stories = self.get_queryset()
        serializer = StorySerializer(stories, many=True, context={'user': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)
