from django.urls import path

from .jwt.views import JWTTokenObtainPairView, JWTTokenRefreshView

urlpatterns = [
    path("jwt/", JWTTokenObtainPairView.as_view(), name="jwt_obtain"),
    path("jwt/refresh/", JWTTokenRefreshView.as_view(), name="jwt_refresh"),
]
