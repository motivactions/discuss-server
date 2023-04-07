import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2Client,
    OAuth2Error,
    OAuth2LoginView,
)
from django.conf import settings

from .provider import AuthenticsProvider


class AuthenticsOauth2Client(OAuth2Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_access_token(self, code, pkce_code_verifier=None):
        from providers.authentics import code_verifier

        data = {
            "redirect_uri": self.callback_url,
            "grant_type": "authorization_code",
            "code": code,
        }

        if self.basic_auth:
            auth = requests.auth.HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        else:
            auth = None
            data.update(
                {
                    "client_id": self.consumer_key,
                    "client_secret": self.consumer_secret,
                    "code_verifier": code_verifier,
                }
            )

        self._strip_empty_keys(data)
        url = self.access_token_url

        resp = requests.post(
            url,
            data=data,
            headers=self.headers,
            auth=auth,
        )

        access_token = None

        if resp.status_code not in [200, 201]:
            print(resp.content)

        access_token = resp.json()

        if not access_token or "access_token" not in access_token:
            raise OAuth2Error("Error retrieving access token: %s" % resp.content)
        return access_token


class AuthenticsAdapter(OAuth2Adapter):
    client_class = AuthenticsOauth2Client
    provider_id = AuthenticsProvider.id
    redirect_uri_protocol = "https"

    # Fetched programmatically, must be reachable from container
    access_token_url = "{}/oauth/token/".format(settings.AUTHENTICS_BASEURL)
    profile_url = "{}/oauth/profile/".format(settings.AUTHENTICS_BASEURL)

    # Accessed by the user browser, must be reachable by the host
    authorize_url = "{}/oauth/authorize/".format(settings.AUTHENTICS_BASEURL)

    # NOTE: trailing slashes in URLs are important, don't miss it

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login

    def get_callback_url(self, request, app):
        return super().get_callback_url(request, app)

    def parse_token(self, data):
        token = super().parse_token(data)
        return token


class AuthenticsLoginView(OAuth2LoginView):
    pass


class AuthenticsCallbackView(OAuth2CallbackView):
    pass


oauth2_login = OAuth2LoginView.adapter_view(AuthenticsAdapter)
oauth2_callback = AuthenticsCallbackView.adapter_view(AuthenticsAdapter)
