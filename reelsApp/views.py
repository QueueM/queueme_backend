from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ReelSerializer, CommentSerializer
from .models import ReelsModel, CommentsModel
from .filters import ReelsFilter, CommentsFilter

class ReelsViewSet(CustomBaseModelViewSet):
    queryset = ReelsModel.objects.all().order_by('-created_at')
    serializer_class = ReelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReelsFilter

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        reel = self.get_object()
        if request.user in reel.likes.all():
            reel.likes.remove(request.user)
        else:
            reel.likes.add(request.user)
        serializer = self.get_serializer(reel)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def increment_view(self, request, pk=None):
        reel = self.get_object()
        reel.increment_views()
        serializer = self.get_serializer(reel)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentViewSet(CustomBaseModelViewSet):
    queryset = CommentsModel.objects.filter(parent=None).order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CommentsFilter

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
