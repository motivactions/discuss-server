from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import RefreshToken, TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings


class JWTTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh_token"])
        data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
        return data


class JWTTokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data.update(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }
        )

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
