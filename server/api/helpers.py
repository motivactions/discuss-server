from django.core.exceptions import (
    ImproperlyConfigured,
    NON_FIELD_ERRORS as DJ_NON_FIELD_ERRORS,
)
from django.core.exceptions import ValidationError as DjangoValidationError
from django.urls import include, path, re_path
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView, api_settings
from rest_framework.views import exception_handler as drf_exception_handler
from server import hooks

DRF_NON_FIELD_ERRORS = api_settings.NON_FIELD_ERRORS_KEY


def get_router(hook_name, router=None):
    """Registered viewsets"""
    hook_funcs = hooks.get_hooks(hook_name)
    if router is None:
        router = DefaultRouter()
    for func in hook_funcs:
        hook = func()
        router.register("%s" % hook["prefix"], hook["viewset"], hook["basename"])
    return router


def get_apiview(hook_name):
    urlpatterns = []
    hook_funcs = hooks.get_hooks(hook_name)
    for hook in hook_funcs:
        apiview = hook()
        # Validate apiview dictionary
        if not isinstance(apiview, (dict,)):
            raise TypeError("API_V1_VIEW_HOOK type must be a dict instance!")

        # Validate viewclass
        view_class = apiview.get("view_class", None)
        if view_class is None:
            raise TypeError("API_V1_VIEW_HOOK result must have a 'view_class' key!")
        if not issubclass(view_class, (APIView,)):
            raise ImproperlyConfigured("%s must subclass of DRF APIView!")

        url_path = apiview.get("url_path", None)
        if url_path is None:
            raise TypeError("API_V1_VIEW_HOOK result must have a 'url_path' key!")

        if not isinstance(url_path, (str,)):
            raise ImproperlyConfigured("%s must be a string!")

        regex_path = apiview.get("regex", False)
        path_func = re_path if regex_path else path
        path_name = apiview.get("name", False) or apiview.__class__.__name__.lower()

        urlpatterns.append(path_func(url_path, view_class.as_view(), name=path_name))

    return urlpatterns


def get_urls(hook_name):
    urlpatterns = []
    hook_funcs = hooks.get_hooks(hook_name)
    for hook in hook_funcs:
        url_path, urls_module = hook()
        urlpatterns.append(path(url_path, include(urls_module)))
    return urlpatterns


def error_handler(exc, context):
    # translate django validation error which ...
    # .. causes HTTP 500 status ==> DRF validation which will cause 400 HTTP status
    if isinstance(exc, DjangoValidationError):
        data = exc.message_dict
        if DJ_NON_FIELD_ERRORS in data:
            data[DRF_NON_FIELD_ERRORS] = data[DJ_NON_FIELD_ERRORS]
            del data[DJ_NON_FIELD_ERRORS]

        exc = DRFValidationError(detail=data)

    return drf_exception_handler(exc, context)
