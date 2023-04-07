from rest_framework.routers import DefaultRouter

from server.api.helpers import get_router

from .viewsets import MeGroupViewSet, MePermissionViewSet, MeProfileViewSet

router = DefaultRouter()
router.register("group", MeGroupViewSet, "megroup")
router.register("permission", MePermissionViewSet, "mepermission")

get_router("API_V1_ME_VIEWSET", router=router)

router.register("", MeProfileViewSet, "meprofile")

urlpatterns = []

urlpatterns += router.urls
