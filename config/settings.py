import os
import tomllib
import cloudinary
from pathlib import Path
from datetime import timedelta


# ----------------------------------------------------------------------
# 0. SETUP
# ----------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "env.toml", mode="rb") as env_file:
    env = tomllib.load(env_file)

# ----------------------------------------------------------------------
# 1. DJANGO CORE SETTINGS
# ----------------------------------------------------------------------

# DEBUGGING

DEBUG = env["core"]["debug"]

# CORE

ALLOWED_HOSTS = env["core"]["allowed_hosts"]

# SECURITY
SECRET_KEY = env["core"]["secret_key"]

# MODELS

INSTALLED_APPS = [
    "apps.users",
    "apps.posts",
    "apps.api",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
]

# HTTP

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = ["localhost", "127.0.0.1"]

WSGI_APPLICATION = "config.wsgi.application"

# URLs

ROOT_URLCONF = "config.urls"

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


# DATABASES
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env["database"]["PGDATABASE"],
        "USER": env["database"]["PGUSER"],
        "PASSWORD": env["database"]["PGPASSWORD"],
        "HOST": env["database"]["PGHOST"],
        "PORT": env["database"]["PGPORT"],
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

# GLOBALIZATION

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en-us", "English"),
    ("es", "Spanish"),
]

USE_I18N = True

USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = ","

TIME_ZONE = "America/El_Salvador"

USE_TZ = True

# FILE UPLOADS

MEDIA_URL = "/uploads/"

MEDIA_ROOT = os.path.join(BASE_DIR, env["file_uploads"]["media_root"])

# LOGGING

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "rich": {"datefmt": "[%X]"},
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "filters": ["require_debug_true"],
            "formatter": "rich",
            "level": "DEBUG",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
    },
    "loggers": {
        "django": {
            "handlers": [],
            "level": "INFO",
        },
        "django.db.backends": {
            "handlers": ["console"],
            # "level": "DEBUG",  # TODO: remove on prod.
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# ----------------------------------------------------------------------
# 2. DJANGO CONTRIB SETTINGS
# ----------------------------------------------------------------------


# AUTH

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{validator}"}
    for validator in (
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator",
    )
]


AUTH_USER_MODEL = "users.User"
CORS_ORIGIN_ALLOW_ALL = True
CARS_ALLOW_CREDENTIALS = True

# OTHERS

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = "static/"

# ----------------------------------------------------------------------
# 3. THIRD PARTY APPS SETTINGS
# ----------------------------------------------------------------------

# DJANGO REST FRAMEWORK

# noinspection PyUnresolvedReferences
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "EXCEPTION_HANDLER": "common.api.api_exception_http",
    "DATETIME_INPUT_FORMATS": ["%Y-%m-%dT%I:%M:%S %p", "iso-8601"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# API JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=5),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}


# Cloudinary
cloudinary.config(
    cloud_name=env["cloudinary"]["CLOUDINARY_NAME"],
    api_key=env["cloudinary"]["CLOUDINARY_API"],
    api_secret=env["cloudinary"]["CLOUDINARY_SECRET"],
    secure=True,
)

# DJANGO SPECTACULAR

SPECTACULAR_SETTINGS = {
    "TITLE": "Instaclone API",
    "DESCRIPTION": (
        "Instaclone API endpoints specification.<br><br>"
        "Base URL: http://127.0.0.1:8000/ <br><br>"
        "**Error responses** <br>"
        "All error responses will return a JSON object with the single key `errors` "
        "containing relevant information describing the problem. When possible, "
        "errors will be keyed with the corresponding erroneous fields. "
        "Otherwise, non-field-errors will be properly indicated."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "GROUPING": "TAG",
    "REDOC_UI_SETTINGS": {
        "hideDownloadButton": True,
        "sortTagsAlphabetically": True,
        "pathInMiddlePanel": True,
        "disableSearch": False,
        "theme": {
            "typography": {
                "fontWeightBold": 700,
            },
            "sidebar": {"backgroundColor": "#f8f9fa"},
            "rightPanel": {"backgroundColor": "#2c3e50", "width": "30%"},
        },
    },
    "REDOC_DIST": "SIDECAR",
    "SORT_OPERATIONS": False,
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": False,
    "TAGS": [
        {"name": "🔑 Auth", "description": "Authentication actions endpoints."},
        {"name": "👥 Users", "description": "Users actions endpoints."},
        {"name": "📸 Publications", "description": "Publications actions endpoints."},
        {"name": "🩷 Likes", "description": "Likes actions endpoints."},
    ],
}

# ----------------------------------------------------------------------
# 4. PROJECT SETTINGS
# ----------------------------------------------------------------------

API_URL = "/api/"
