import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet


from . import filtersets, serializers

logger = logging.getLogger(__name__)

User = get_user_model()


class PermissionViewSet(ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = serializers.PermissionSerializer

    @extend_schema(operation_id="users_permission_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="users_permission_detail")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer

    @extend_schema(operation_id="users_group_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="users_group_detail")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ["pk", "last_login"]
    search_fields = ["$username", "$first_name", "$last_name"]
    filterset_class = filtersets.UserAPIFilterset

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if self.action == "list" and not user.is_staff:
            return qs.filter(pk=user.id)
        return qs

    @extend_schema(operation_id="users_user_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="users_user_detail")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class MeProfileViewSet(GenericViewSet):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action in ["profile"]:
            return serializers.UserSerializer
        elif self.action in ["profile_update", "profile_update_partial"]:
            return serializers.UserUpdateSerializer
        else:
            return super().get_serializer_class()

    @extend_schema(
        operation_id="profile_retrieve",
        responses=serializers.UserSerializer,
    )
    @action(methods=["GET"], url_path="profile", detail=False)
    def profile(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id="profile_update",
        responses=serializers.UserSerializer,
    )
    @action(methods=["PUT"], url_path="profile/update", detail=False)
    def profile_update(self, request, pk=None, *args, **kwargs):
        kwargs["partial"] = False
        return self.perform_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="profile_update_partial",
        responses=serializers.UserSerializer,
    )
    @action(methods=["PATCH"], url_path="profile/update", detail=False)
    def profile_update_partial(self, request, pk=None, *args, **kwargs):
        kwargs["partial"] = True
        return self.perform_update(request, *args, **kwargs)

    def perform_update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        resp_serializer = serializers.UserSerializer(
            instance=obj, context=self.get_serializer_context()
        )
        return Response(resp_serializer.data)


class MeGroupViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.GroupSerializer

    def get_queryset(self):
        return self.request.user.groups.all()

    @extend_schema(operation_id="group_list")
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer_class()(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(operation_id="group_retrieve")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class MePermissionViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.PermissionSerializer

    def get_queryset(self):
        return self.request.user.user_permissions.all()

    @extend_schema(operation_id="permission_list")
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer_class()(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(operation_id="permission_retrieve")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
