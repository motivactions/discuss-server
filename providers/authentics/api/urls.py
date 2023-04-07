from django.urls import path

from .views import (
    LoginURL,
    TokenObtainView,
    TokenRefreshView,
)

urlpatterns = [
    path("login/", LoginURL.as_view(), name="authentics_login"),
    path("obtain/", TokenObtainView.as_view(), name="authentics_obtain_token"),
    path("refresh/", TokenRefreshView.as_view(), name="authentics_refresh_token"),
]
