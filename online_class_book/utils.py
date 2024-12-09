from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import NotAuthenticated
from rest_framework import status


# Helper for return response
def get_response(code_status, msg, payload):
    return Response( {'status': code_status, 'msg': msg, 'data': payload }, status=code_status)


# Custom error for authentication
def custom_token_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if (isinstance(exc, InvalidToken)) or (isinstance(exc, NotAuthenticated)):
        return get_response(status.HTTP_401_UNAUTHORIZED, 'Invalid Access key.', {})

    return response
