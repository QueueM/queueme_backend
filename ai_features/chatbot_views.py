from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .chatbot import process_chat_message

class ChatbotAPIView(APIView):
    """
    POST: Accepts a chat message and returns a chatbot response.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        message = request.data.get("message", "")
        if not message:
            return Response({"error": "No message provided."}, status=400)
        response_message = process_chat_message(message)
        return Response({"response": response_message})
