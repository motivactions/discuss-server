from rest_framework import serializers
from ...models import Application, ApplicationKey


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


class ApplicationKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationKey
        fields = "__all__"
