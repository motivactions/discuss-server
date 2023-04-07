from rest_framework.routers import DefaultRouter

from .viewsets import GroupViewSet, PermissionViewSet, UserViewSet

router = DefaultRouter()
router.register("user", UserViewSet, "user")
router.register("group", GroupViewSet, "group")
router.register("permission", PermissionViewSet, "permission")

urlpatterns = []

urlpatterns += router.urls
