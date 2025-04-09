from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .image_analysis import analyze_image

class ImageAnalysisAPIView(APIView):
    """
    POST: Accepts an image file and returns analysis results.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No image uploaded."}, status=400)
        image_file = request.FILES['image']
        temp_path = 'temp_image.jpg'
        with open(temp_path, 'wb+') as f:
            for chunk in image_file.chunks():
                f.write(chunk)
        try:
            results = analyze_image(temp_path)
            return Response({"analysis": results})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
