import os
from datetime import timedelta

from .base import BASE_DIR, BASE_URL, PROJECT_NAME

API_DESCRIPTION = """# Introduction.

## Authentication and Authorization

This API offers several forms of authentication:

- BasicAuth
- TokenAuthentication
- Cookie Authentication
- JWT Authentication
- OAuth2
  OAuth2 - an open protocol to allow secure authorization in a simple
  and standard method from web, mobile and desktop applications.
"""


##############################################################################
# REST FRAMEWORK
##############################################################################

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=90),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=90),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=90),
}

DEFAULT_RENDERER_CLASSES = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

REST_FRAMEWORK = {
    "PAGE_SIZE": 50,
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "EXCEPTION_HANDLER": "server.api.helpers.error_handler",
    "DEFAULT_SCHEMA_CLASS": "server.api.schemas.CustomAutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "providers.authentics.api.authentication.AuthenticsOauth",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework_api_key.permissions.HasAPIKey",
    ],
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}


##############################################################################
# DOCUMENTATIONS
##############################################################################

DOCS_SOURCE = os.path.join(BASE_DIR, "docs", "source")
DOCS_ROOT = os.path.join(BASE_DIR, "docs", "build", "html")

SPECTACULAR_SETTINGS = {
    "CAMELIZE_NAMES": True,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "DEFAULT_GENERATOR_CLASS": "server.api.schemas.CustomSchemaGenerator",
    "TITLE": PROJECT_NAME + " API",
    "DESCRIPTION": API_DESCRIPTION,
    "TOS": None,
    "CONTACT": {
        "name": PROJECT_NAME,
        "url": BASE_URL,
        "email": "sasri.project@gmail.com",
    },
    # Optional: MUST contain "name", MAY contain URL
    "LICENSE": {},
    # Statically set schema version. May also be an empty string. When used together
    # view versioning, will become '0.0.0 (v2)' for 'v2' versioned requests.
    # Set VERSION to None if only the request version should be rendered.
    "VERSION": None,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    # Optional list of servers.
    # Each entry MUST contain "url", MAY contain "description", "variables"
    # e.g. [{'url': 'https://example.com/v1', 'description': 'Text'}, ...]
    "SERVERS": [
        {
            "url": BASE_URL,
            "description": PROJECT_NAME + "Service",
        }
    ],
    # Tags defined in the global scope
    "TAGS": [
        # {
        #     "name": "user",
        #     "description": "User is awesome",
        # }
    ],
    # Optional: MUST contain 'url', may contain "description"
    "EXTERNAL_DOCS": {},
    # Arbitrary specification extensions attached to the schema's info object.
    # https://swagger.io/specification/#specification-extensions
    "EXTENSIONS_INFO": {
        "x-logo": {
            "url": "/static/theme_default/img/logo/logo_api.svg",
            "backgroundColor": "#FFFFFF",
            "altText": "Example logo",
        },
    },
    # Arbitrary specification extensions attached to the schema's root object.
    # https://swagger.io/specification/#specification-extensions
    "EXTENSIONS_ROOT": {
        # "x-tagGroups": [
        #     {
        #         "name": "General",
        #         "tags": ["user", "category", "tag"],
        #     },
        # ],
    },
    "SERVE_AUTHENTICATION": ("rest_framework.authentication.SessionAuthentication",),
}
