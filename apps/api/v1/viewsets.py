import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ...models import Application, ApplicationKey
from .serializers import ApplicationSerializer, ApplicationKeySerializer

logger = logging.getLogger(__name__)


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_serializer_class(self):
        return super().get_serializer_class()

    @extend_schema(operation_id="application_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="application_retrieve")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(operation_id="application_create")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(operation_id="application_update")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(operation_id="application_update_partial")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(operation_id="application_destroy")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
