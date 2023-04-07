from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from providers.authentics import code_challenge


class AuthenticsAccount(ProviderAccount):
    pass


class AuthenticsProvider(OAuth2Provider):
    id = "authentics"
    name = "Authentics"
    account_class = AuthenticsAccount

    def extract_uid(self, data):
        return str(data["id"])

    def extract_common_fields(self, data):
        return dict(
            username=data["username"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )

    def get_login_url(self, request, **kwargs):
        login_url = super().get_login_url(request, **kwargs)
        return login_url

    def get_auth_params(self, request, action):
        params = super().get_auth_params(request, action)
        extra_params = {
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        params.update(extra_params)
        return params

    def get_default_scope(self):
        scope = ["read"]
        return scope

    def sociallogin_from_response(self, request, response):
        return super().sociallogin_from_response(request, response)


providers.registry.register(AuthenticsProvider)
