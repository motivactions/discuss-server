import base64
import hashlib
import logging
import random
import string
from urllib import parse

import requests
from django.conf import settings

code_verifier = "".join(
    random.choice(string.ascii_uppercase + string.digits)
    for _ in range(random.randint(43, 128))
)
code_verifier = base64.urlsafe_b64encode(code_verifier.encode("utf-8"))
code_challenge = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8").rstrip("=")

logger = logging.getLogger(__name__)

TOKEN_PREFIX = getattr(settings, "AUTHENTICS_TOKEN_PREFIX", "Bearer")
BASE_URL = settings.AUTHENTICS_API_URL
CLIENT_ID = settings.AUTHENTICS_CLIENT_ID
CLIENT_SECRET = settings.AUTHENTICS_CLIENT_SECRET
REDIRECT_URL = settings.AUTHENTICS_REDIRECT_URL
API_KEY = settings.AUTHENTICS_API_KEY

GRANT_REFRESH_TOKEN = "refresh_token"
GRANT_AUTHORIZATION_CODE = "authorization_code"


class AuthenticClient:
    def get_login_url(self, next=None):
        params = {
            "response_type": "code",
            "code_challenge": code_challenge,
            "code_verifier": code_verifier,
            "code_challenge_method": "S256",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URL,
        }
        path = BASE_URL + "/api/oauth/authorize/"
        login_url = path + "?" + parse.urlencode(params)
        return login_url

    def get_token(self, grant_type, authorization_code=None, refresh_token=None):
        # Get access token
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code_verifier": code_verifier.decode("utf-8"),
            "grant_type": grant_type,
        }
        if grant_type == GRANT_AUTHORIZATION_CODE and authorization_code is not None:
            payload.update(
                {
                    "code": authorization_code,
                    "redirect_uri": REDIRECT_URL,
                }
            )
        if grant_type == GRANT_REFRESH_TOKEN and refresh_token is not None:
            payload.update(
                {
                    "refresh_token": refresh_token,
                }
            )
        resp = requests.post(BASE_URL + "/api/oauth/token/", data=payload)
        return resp

    def obtain_access_token(self, authorization_code=None):
        return self.get_token(
            grant_type=GRANT_AUTHORIZATION_CODE,
            authorization_code=authorization_code,
        )

    def refresh_access_token(self, refresh_token=None):
        return self.get_token(
            grant_type=GRANT_REFRESH_TOKEN,
            refresh_token=refresh_token,
        )

    def get_user_profile(self, access_token):
        url = BASE_URL + "/api/oauth/profile/"
        headers = {
            "X-Api-Key": API_KEY,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        resp = requests.request("GET", url, headers=headers, data={})
        return resp


authentics = AuthenticClient()
