from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    try:
        if response is None:
            return Response({"message": str(exc)}, status=500)
        if isinstance(response.data, dict):
            if 'message' not in response.data:
                message_parts = []
                for field, errors in response.data.items():
                    if isinstance(errors, list):
                        message_parts.append(f"{field} : {', '.join(errors)}")
                if message_parts:
                    response.data['message'] = ', '.join(message_parts)
            elif isinstance(response.data.get('message'), list):
                response.data['message'] = response.data['message'][0]
        elif isinstance(response.data, list):
            response.data = {"message": ', '.join(response.data)}
    except Exception as e:
        pass
    return response
