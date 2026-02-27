from rest_framework.response import Response
from rest_framework import status as http_status


def success_response(data=None, message='Success', status_code=http_status.HTTP_200_OK):
    """
    Utility function for consistent success response formatting.
    Format: {"success": true, "message": "...", "data": {...}}
    """
    response_data = {
        'success': True,
        'message': message,
        'data': data,
    }
    return Response(response_data, status=status_code)
