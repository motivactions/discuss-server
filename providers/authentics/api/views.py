from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from requests.exceptions import JSONDecodeError
from rest_framework.response import Response
from rest_framework.views import APIView

from ..clients import authentics
from .exceptions import AuthenticationFailed
from .serializers import (
    LoginSerializer,
    ObtainTokenSerializer,
    RefreshTokenSerializer,
    TokenSerializer,
)

User = get_user_model()


class LoginURL(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        operation_id="authentics_login",
        request=None,
        responses=LoginSerializer,
    )
    def get(self, *args, **kwargs):
        """return login url for authentics"""
        return Response({"url": authentics.get_login_url(next)})


class TokenObtainView(APIView):
    authentication_classes = []
    permission_classes = []

    def get_serializer(self, **kwargs):
        serializer = ObtainTokenSerializer(**kwargs)
        return serializer

    def get_response_serializer(self, **kwargs):
        serializer = TokenSerializer(**kwargs)
        return serializer

    def get_serializer_context(self):
        return {}

    @extend_schema(
        operation_id="authentics_obtain_token",
        request=ObtainTokenSerializer,
        responses=TokenSerializer,
    )
    def post(self, *args, **kwargs):
        """Obtain access token"""
        serializer = self.get_serializer(
            data=self.request.data,
            context={"context": self.get_serializer_context()},
        )
        serializer.is_valid(raise_exception=True)

        resp = authentics.obtain_access_token(
            authorization_code=serializer.data["authorization_code"]
        )
        if resp.status_code not in [200, 201]:
            try:
                resp_json = resp.json()
                print(resp_json)
                msg = resp_json.get("detail", "Failed to obtain the token.")
                raise AuthenticationFailed(msg)
            except JSONDecodeError:
                msg = str(resp.content)
                raise AuthenticationFailed(msg)

        resp_json = resp.json()
        resp_serializer = self.get_response_serializer(data=resp_json)
        resp_serializer.is_valid(raise_exception=True)

        return Response(resp_serializer.data, status=200)


class TokenRefreshView(APIView):
    authentication_classes = []
    permission_classes = []

    def get_serializer(self, **kwargs):
        serializer = RefreshTokenSerializer(**kwargs)
        return serializer

    def get_response_serializer(self, **kwargs):
        serializer = TokenSerializer(**kwargs)
        return serializer

    def get_serializer_context(self):
        return {}

    @extend_schema(
        operation_id="authentics_refresh_token",
        request=RefreshTokenSerializer,
        responses=TokenSerializer,
    )
    def post(self, request, *args, **kwargs):
        """Refresh access token"""
        serializer = self.get_serializer(
            data=self.request.data,
            context={"context": self.get_serializer_context()},
        )
        serializer.is_valid(raise_exception=True)
        resp = authentics.refresh_access_token(
            refresh_token=serializer.data["refresh_token"]
        )
        if resp.status_code not in [200, 201]:
            try:
                resp_json = resp.json()
                msg = resp_json.get("detail", "Failed to refresh the token.")
                raise AuthenticationFailed(msg)
            except JSONDecodeError:
                msg = str(resp.content)
                raise AuthenticationFailed(msg)

        resp_json = resp.json()
        resp_serializer = self.get_response_serializer(data=resp_json)
        resp_serializer.is_valid(raise_exception=True)

        return Response(resp_serializer.data, status=200)
