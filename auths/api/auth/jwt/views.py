from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import JWTTokenObtainPairSerializer, JWTTokenRefreshSerializer

User = get_user_model()


class JWTTokenObtainPairView(TokenObtainPairView):
    serializer_class = JWTTokenObtainPairSerializer

    @extend_schema(responses=JWTTokenObtainPairSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class JWTTokenRefreshView(TokenRefreshView):
    serializer_class = JWTTokenRefreshSerializer

    @extend_schema(responses=JWTTokenRefreshSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
