from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    expires_in = serializers.IntegerField(required=True)
    token_type = serializers.CharField(required=True)
    scope = serializers.CharField(required=True)
    refresh_token = serializers.CharField(required=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        return data


class LoginSerializer(serializers.Serializer):
    url = serializers.URLField()


class ObtainTokenSerializer(serializers.Serializer):
    authorization_code = serializers.CharField(required=True)


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
