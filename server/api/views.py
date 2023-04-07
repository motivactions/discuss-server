from drf_spectacular.views import SpectacularAPIView as BaseSpectacularAPIView
from drf_spectacular.views import SpectacularRedocView as BaseSpectacularRedocView

from .schemas import CustomSchemaGenerator


class SpectacularAPIView(BaseSpectacularAPIView):
    authentication_classes = []
    generator_class = CustomSchemaGenerator


class SpectacularRedocView(BaseSpectacularRedocView):
    authentication_classes = []
