import os
from pathlib import Path

DEBUG = True

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8001")

PROJECT_NAME = "Notice Server"

PROJECT_DIR = BASE_DIR / "server"

SECRET_KEY = "django-insecure-b(j+w&tmv6cq2&ufdo=@4(35-5qag-ahi6(gw(d^oaednfdo(h"

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "apps",
    "auths",
    "discuss",
    "providers.authentics",
    "providers.authentics.api",
    # Dependencies
    "mptt",
    "easy_thumbnails",
    "rest_framework",
    "rest_framework_api_key",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
    # Django
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_cleanup",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"


##############################################################################
# DATABASE
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
##############################################################################

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

##############################################################################
# AUTHENTICATIONS
##############################################################################


AUTHENTICS_BASEURL = "https://oauth2.dev-tunnel.mitija.com"

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "authentics": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": "p09nQOLOf2HdOnz20N3kaU951hIBy7BaeLtwuRgQ",
            "secret": "sFkW2I337wddbF97unLoue3A7PZ3hrCF4joLUVtBgEupom634bpIW0FhKQ7dkQlhzlWqk1ptXgSNKi8soHxx3HXigyEWQOmjKILUOk16lxqihEg5088nKf1mlmKhVI9Y",
            "key": "",
        }
    }
}

# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = "auths.User"
AUTH_VALIDATORS = "django.contrib.auth.password_validation."
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": AUTH_VALIDATORS + "UserAttributeSimilarityValidator"},
    {"NAME": AUTH_VALIDATORS + "MinimumLengthValidator"},
    {"NAME": AUTH_VALIDATORS + "CommonPasswordValidator"},
    {"NAME": AUTH_VALIDATORS + "NumericPasswordValidator"},
]

# Authentication Service
AUTHENTICS_API_KEY = os.getenv("AUTHENTICS_API_KEY", "")
AUTHENTICS_CLIENT_ID = os.getenv("AUTHENTICS_CLIENT_ID", "")
AUTHENTICS_CLIENT_SECRET = os.getenv("AUTHENTICS_CLIENT_SECRET", "")
AUTHENTICS_REDIRECT_URL = os.getenv("AUTHENTICS_REDIRECT_URL", "")
AUTHENTICS_API_URL = os.getenv("AUTHENTICS_API_URL", "")

##############################################################################
# NOTIFICATIONS
##############################################################################

# TODO Setup notification Service

##############################################################################
# INTERNATIONALIZATION
# https://docs.djangoproject.com/en/4.0/topics/i18n/
##############################################################################

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_L10N = True
USE_TZ = True

##############################################################################
# STATICFILE & STORAGE
##############################################################################

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
MEDIA_URL = "/media/"

##############################################################################
# EMAIL
##############################################################################

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
