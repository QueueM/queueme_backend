

from rest_framework.views import exception_handler
from rest_framework.response import Response
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    try :
        # if response data is dict
        if response is None:
            # If response is None, return a generic error response
            return Response(
                {"message": str(exc)},
                status=500
            )

        if response is not None and isinstance(response.data, dict):
            # Ensure the message key is a string, not a list
            if 'message' not in response.data:
                # If no "message" key, create it by iterating over the fields with errors
                message_parts = []

                for field, errors in response.data.items():
                    # Only add error fields to the message if they are lists
                    if isinstance(errors, list):
                        message_parts.append(f"{field} : {', '.join(errors)}")
                
                # If there are any errors, join them into a single string and add to "message"
                if message_parts:
                    response.data['message'] = ', '.join(message_parts)
            
            elif isinstance(response.data.get('message'), list):
                response.data['message'] = response.data['message'][0]
        elif isinstance(response.data, list):
            obj={"message":', '.join(response.data)}
            response.data = obj 
        print(type(response.data))
    except Exception as e:
        pass
    return response