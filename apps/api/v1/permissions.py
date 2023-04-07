from rest_framework.permissions import BasePermission
from rest_framework_api_key.permissions import BaseHasAPIKey
from rest_framework_api_key.models import APIKey
from ...models import Application


class IsStaffUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and (request.user.is_staff or request.user.is_superuser)
        )


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # must be the owner to view the object
        owner = getattr(obj, "user", None)
        user = getattr(obj, "owner", None)
        return (owner == request.user) or (user == request.user)


class HasApplicationKey(BasePermission):
    def has_permission(self, request, view):
        application = Application.get_from_request_headers(request)
        return bool(application)


class HasApplicationAPIKey(BaseHasAPIKey):
    model = APIKey

    def has_permission(self, request, view) -> bool:
        # Check Application Key
        application = Application.get_from_request_headers(request)
        if not application:
            return False

        # Check API Key linked with application
        key = self.get_key(request)
        if key is None:
            return False

        try:
            apikey = self.model.objects.get_from_key(key)
            valid_key = self.model.objects.is_valid(key)
        except APIKey.DoesNotExist:
            return False

        # Check API Key linked with application
        if not apikey or not valid_key:
            return False

        aplication_api_key = application.apikeys.filter(id=apikey.id).first()
        return bool(aplication_api_key)
