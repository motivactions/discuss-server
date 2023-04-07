from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework_api_key.models import APIKey
from apps.api.v1 import permissions
from apps.models import Application, ApplicationKey

User = get_user_model()


class RequestObject:
    def __init__(self, user) -> None:
        self.user = user


class UserObject:
    def __init__(self, user) -> None:
        self.user = user


class OwnerObject:
    def __init__(self, owner) -> None:
        self.owner = owner


class ViewObject:
    def __init__(self) -> None:
        pass


class TestSendNotification(TestCase):
    def setUp(self) -> None:
        self.view = ViewObject()
        # Init Users
        self.user1 = User.objects.create_user(username="testuser1", password="test123")
        self.user2 = User.objects.create_user(username="testuser2", password="test123")
        self.user_staff = User.objects.create_user(
            username="test_staff_user",
            password="test123",
            is_staff=True,
        )
        self.user_admin = User.objects.create_user(
            username="test_admin_user",
            password="test123",
            is_superuser=True,
        )

        # Create Application
        self.application = Application(
            owner=self.user1,
            name="Application Test",
            domain="http://localhost:8000",
        )
        self.application.save()

        # Create API Key
        api_key1, key1 = self.api_key = APIKey.objects.create_key(name="Test API Key")
        self.api_key1 = key1
        self.api_key_object1 = api_key1

        # Create API Key
        api_key2, key2 = self.api_key = APIKey.objects.create_key(name="Test API Key")
        self.api_key2 = key2
        self.api_key_object2 = api_key2

        # Link API Key to Application
        self.application.apikeys.add(self.api_key_object1)

        return super().setUp()

    def test_is_owner(self):
        request1 = RequestObject(self.user1)
        request2 = RequestObject(self.user2)

        user_object = UserObject(self.user1)
        owner_object = OwnerObject(self.user1)

        is_owner = permissions.IsOwner()

        has_perm = is_owner.has_permission(request1, self.view)
        self.assertTrue(has_perm)

        has_obj_perm = is_owner.has_object_permission(request1, self.view, user_object)
        self.assertTrue(has_obj_perm)

        has_obj_perm = is_owner.has_object_permission(request2, self.view, user_object)
        self.assertFalse(has_obj_perm)

        has_obj_perm = is_owner.has_object_permission(request1, self.view, owner_object)
        self.assertTrue(has_obj_perm)

        has_obj_perm = is_owner.has_object_permission(request2, self.view, owner_object)
        self.assertFalse(has_obj_perm)

    def test_is_admin_user(self):
        perm = permissions.IsAdminUser()

        request = RequestObject(self.user_admin)
        has_perm = perm.has_permission(request, self.view)
        self.assertTrue(has_perm)

        request = RequestObject(self.user_staff)
        has_perm = perm.has_permission(request, self.view)
        self.assertFalse(has_perm)

        request = RequestObject(self.user1)
        has_perm = perm.has_permission(request, self.view)
        self.assertFalse(has_perm)

    def test_is_staff_user(self):
        perm = permissions.IsStaffUser()

        request = RequestObject(self.user_admin)
        has_perm = perm.has_permission(request, self.view)
        self.assertTrue(has_perm)

        request = RequestObject(self.user_staff)
        has_perm = perm.has_permission(request, self.view)
        self.assertTrue(has_perm)

        request = RequestObject(self.user1)
        has_perm = perm.has_permission(request, self.view)
        self.assertFalse(has_perm)

    def test_has_aplication_key(self):
        perm = permissions.HasApplicationKey()
        request = RequestObject(self.user1)

        request.headers = {"X-Application": self.application.id}
        request.META = {"HTTP_X_APPLICATION": self.application.id}
        has_perm = perm.has_permission(request, self.view)
        self.assertTrue(has_perm)

        request.headers = {"X-Application": "WrongApplicationKey"}
        request.META = {"HTTP_X_APPLICATION": "WrongApplicationKey"}
        has_perm = perm.has_permission(request, self.view)
        self.assertFalse(has_perm)

        request.headers = {}
        request.META = {}
        has_perm = perm.has_permission(request, self.view)
        self.assertFalse(has_perm)

    def test_has_aplication_api_key(self):
        perm = permissions.HasApplicationAPIKey()
        request = RequestObject(self.user1)

        # Test Linked API Key
        request.headers = {
            "X-Application": self.application.id,
            "X-Api-Key": self.api_key1,
        }
        request.META = {
            "HTTP_X_APPLICATION": self.application.id,
            "HTTP_X_API_KEY": self.api_key1,
        }
        has_perm = perm.has_permission(request, self.view)
        self.assertTrue(has_perm)

        # Test Not Linked API Key
        request.headers = {
            "X-Application": self.application.id,
            "X-Api-Key": self.api_key2,
        }
        request.META = {
            "HTTP_X_APPLICATION": self.application.id,
            "HTTP_X_API_KEY": self.api_key2,
        }
        has_perm = perm.has_permission(request, self.view)
        self.assertFalse(has_perm)

        # Test No API Key
        request.headers = {"X-Application": self.application.id}
        request.META = {"HTTP_X_APPLICATION": self.application.id}
        has_perm = perm.has_permission(request, self.view)
        self.assertFalse(has_perm)

        # Test No Application Key
        request.headers = {"X-Api-Key": self.api_key2}
        request.META = {"HTTP_X_API_KEY": self.api_key2}
        has_perm = perm.has_permission(request, self.view)
        self.assertFalse(has_perm)

        # Test No API Key
        request.headers = {"X-Application": "WrongApplicationKey"}
        request.META = {"HTTP_X_APPLICATION": "WrongApplicationKey"}
        has_perm = perm.has_permission(request, self.view)
        self.assertFalse(has_perm)
