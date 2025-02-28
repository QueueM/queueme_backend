from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ReelsModel, CommentsModel
from .serializers import ReelSerializer, CommentSerializer
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
class ReelsViewSet(CustomBaseModelViewSet):
    queryset = ReelsModel.objects.all().order_by('-created_at')
    serializer_class = ReelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user  # Pass the user into the context
        return context
    
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        reel = self.get_object()
        if request.user in reel.likes.all():
            reel.likes.remove(request.user)
            serializer = ReelSerializer(reel)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = ReelSerializer(reel)
            reel.likes.add(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

class CommentViewSet(CustomBaseModelViewSet):
    queryset = CommentsModel.objects.filter(parent=None).order_by('-created_at')  # Only fetch top-level comments
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['POST'])
    def reply(self, request, pk=None):
        parent_comment = self.get_object()
        text = request.data.get('text')

        if not text:
            return Response({"message": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)

        reply = CommentsModel.objects.create(user=request.user, reel=parent_comment.reel, text=text, parent=parent_comment)
        return Response(CommentSerializer(reply).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        comment = self.get_object()
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            serializer = ReelSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            comment.likes.add(request.user)
            serializer = ReelSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
