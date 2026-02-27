import logging
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError,
    NotFound,
    PermissionDenied,
    AuthenticationFailed,
    NotAuthenticated,
    MethodNotAllowed,
    Throttled,
)
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger('freelance_arena')


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent JSON error responses.
    Format: {"success": false, "errors": {...}, "message": "..."}
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {
            'success': False,
            'message': '',
            'errors': {},
        }

        if isinstance(exc, ValidationError):
            custom_response['message'] = 'Validation error.'
            custom_response['errors'] = response.data
        elif isinstance(exc, NotFound):
            custom_response['message'] = 'Resource not found.'
            custom_response['errors'] = {'detail': str(exc.detail)}
        elif isinstance(exc, PermissionDenied):
            custom_response['message'] = 'Permission denied.'
            custom_response['errors'] = {'detail': str(exc.detail)}
        elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
            custom_response['message'] = 'Authentication failed.'
            custom_response['errors'] = {'detail': str(exc.detail)}
        elif isinstance(exc, MethodNotAllowed):
            custom_response['message'] = 'Method not allowed.'
            custom_response['errors'] = {'detail': str(exc.detail)}
        elif isinstance(exc, Throttled):
            custom_response['message'] = 'Request was throttled.'
            custom_response['errors'] = {'detail': str(exc.detail)}
        else:
            custom_response['message'] = 'An error occurred.'
            custom_response['errors'] = response.data

        response.data = custom_response
        return response

    # Handle unhandled exceptions
    logger.exception(f'Unhandled exception: {exc}')
    return Response(
        {
            'success': False,
            'message': 'An internal server error occurred.',
            'errors': {'detail': 'Internal server error.'},
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
