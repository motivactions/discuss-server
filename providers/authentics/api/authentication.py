# from pprint import pprint
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from requests.exceptions import JSONDecodeError
from rest_framework.authentication import BaseAuthentication

from ..clients import authentics, TOKEN_PREFIX
from .exceptions import AuthenticationFailed


class AuthenticsOauth(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        # check authorization header and extract auth token
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header:
            msg = _("No authorization header provided.")
            return None

        access_token = auth_header.split(sep=" ").pop()
        if access_token in ["", None]:
            msg = _("Authorization token is not provided.")
            return None

        resp_identity = authentics.get_user_profile(access_token)
        if resp_identity.status_code not in [200, 201]:
            try:
                resp_json = resp_identity.json()
                msg = resp_json.get("detail", "Failed to get user identity.")
                raise AuthenticationFailed(msg)
            except JSONDecodeError:
                msg = str(resp_identity.content)
                raise AuthenticationFailed(msg)

        resp_json = resp_identity.json()
        user_data = {
            "id": resp_json["id"],
            "username": resp_json["username"],
            "email": resp_json["email"],
            "first_name": resp_json["first_name"],
            "last_name": resp_json["last_name"],
        }

        # Get or create user
        user, created = get_user_model().objects.get_or_create(
            id=resp_json["id"], defaults=user_data
        )

        if not created:
            user_data.pop("id")
            for k, v in user_data.items():
                setattr(user, k, v)
            user.save()
            return (user, None)
        else:
            if user.is_active:
                return (user, None)
            else:
                msg = _("Your user is not activated or blocked.")
                raise AuthenticationFailed(msg)
