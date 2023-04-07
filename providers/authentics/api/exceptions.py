from rest_framework import status
from rest_framework.exceptions import APIException, AuthenticationFailed


class InvalidAuthorizationCode(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid authorization code"
    default_code = "invalid_grant"


class NoBearerToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "No authentication token provided"
    default_code = "no_auth_token"


class InvalidBearerToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid authentication token provided"
    default_code = "invalid_token"
