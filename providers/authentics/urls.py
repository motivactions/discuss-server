from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import AuthenticsProvider

urlpatterns = default_urlpatterns(AuthenticsProvider)
