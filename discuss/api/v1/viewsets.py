import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import OpenApiParameter
from apps.api.v1.permissions import HasApplicationAPIKey, IsOwner
from ...models import Discuss, Application
from .serializers import DiscussSerializer, DiscussCreateSerializer

logger = logging.getLogger(__name__)


class DiscussViewSet(ModelViewSet):
    queryset = Discuss.objects.all()
    serializer_class = DiscussSerializer
    permission_classes = [HasApplicationAPIKey]
    serializer_class = DiscussSerializer

    def get_application(self):
        application = Application.get_from_request_headers(self.request)
        return application

    def get_permissions(self):
        if self.action in ["create"]:
            perm_classes = [HasApplicationAPIKey, IsAuthenticated]
            return [perm() for perm in perm_classes]
        elif self.action in ["update", "partial_update", "destroy"]:
            perm_classes = [HasApplicationAPIKey, IsAuthenticated, IsOwner]
            return [perm() for perm in perm_classes]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        application = self.get_application()
        queryset = queryset.filter(application_id=application.id)
        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return DiscussCreateSerializer
        # if self.action == "add_discuss_reaction":
        #     return ReactionableModelAddSerializer
        # elif self.action == "add_discuss_flag":
        #     return FlaggableModelAddSerializer
        return super().get_serializer_class()

    @extend_schema(
        operation_id="discuss_list",
        parameters=[
            OpenApiParameter(
                "object_id",
                str,
                required=True,
                location="query",
                description=_("The object id."),
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        object_id = request.query_params.get("object_id", None)
        queryset = self.get_queryset().filter(object_id=object_id, level=0)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(operation_id="discuss_retrieve")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(operation_id="discuss_create")
    def create(self, request, *args, **kwargs):
        object_id = request.query_params.get("object_id", None)
        if object_id is None:
            raise ValidationError(
                {"object_id": "Query parameter object_id is not provided!"}
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            application=self.get_application(),
            object_id=object_id,
            user=request.user,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(operation_id="discuss_update")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(operation_id="discuss_update_partial")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(operation_id="discuss_destroy")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(operation_id="discuss_children_list")
    @action(methods=["GET"], url_path="childrens", detail=True)
    def discuss_childrens(self, request, *args, **kwargs):
        obj = self.get_object()
        queryset = obj.children.all()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(operation_id="discuss_reaction_add")
    @action(methods=["POST"], url_path="reaction-create", detail=True)
    def add_discuss_reaction(self, request, pk=None, *args, **kwargs):
        """
        Add a reaction to a discuss.
        Required data = {"value":"(reaction_type)"}
        """
        obj = self.get_object()
        value = request.data.get("value")
        if (value, value) not in Discuss.REACTION_TYPES:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        reaction = obj.add_reaction(self, request.user, value)
        return Response(data=reaction)

    @extend_schema(operation_id="discuss_reaction_remove")
    @action(methods=["DELETE"], url_path="reactions-remove", detail=True)
    def remove_discuss_reaction(self, request, *args, **kwargs):
        """Delete a reaction from a discuss"""
        obj = self.get_object()
        reaction = obj.remove_reaction(self, request.user)
        return Response(data=reaction)

    @extend_schema(operation_id="discuss_flag_create")
    @action(methods=["POST"], url_path="flag-create", detail=True)
    def add_discuss_flag(self, request, pk=None, *args, **kwargs):
        """
        Add a flag to a club.
        Required data = {"value":"(flag_type)"}
        """
        obj = self.get_object()
        value = request.data.get("value")
        if (value, value) not in Discuss.FLAG_TYPES:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        flag = obj.add_flag(self, request.user, value)
        return Response(data=flag)

    @extend_schema(operation_id="discuss_flag_remove")
    @action(methods=["DELETE"], url_path="flags-remove", detail=True)
    def remove_discuss_flag(self, request, pk=None, *args, **kwargs):
        """Delete a flag from a discuss"""
        obj = self.get_object()
        flag = obj.remove_flag(self, request.user)
        return Response(data=flag)
