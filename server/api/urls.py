from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("v1/", include("server.api.endpoints.v1")),
    path("v2/", include("server.api.endpoints.v2")),
]
