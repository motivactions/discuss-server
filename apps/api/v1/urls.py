from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register("applications", viewsets.ApplicationViewSet, "application")

urlpatterns = [] + router.urls
