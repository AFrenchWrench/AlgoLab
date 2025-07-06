from pathlib import Path
from decouple import config, Csv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

SECRET_KEY = config("SECRET_KEY")

# Debug mode toggle
DEBUG = config("DEBUG", default=True, cast=bool)

# Allowed hosts (comma separated in .env)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

INSTALLED_APPS = [
    # Django defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "strawberry.django",
    # Project apps
    "core",
    "api",
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

ROOT_URLCONF = "config.urls"

# We probably won't have templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database (PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = config("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery config
CELERY_BROKER_URL = config("REDIS_URL", default="redis://localhost:6379")
CELERY_RESULT_BACKEND = config("REDIS_URL", default="redis://localhost:6379")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# Strawberry GraphQL settings (optional)
STRAWBERRY_DJANGO = {
    # Add configs if needed
}

# Logging (basic setup)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {module} {process:d} {thread:d} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        },
        "file_info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "info.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "level": "INFO",
        },
        "file_error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "error.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "level": "ERROR",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file_info", "file_error"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file_error", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "core": {
            "handlers": ["console", "file_info", "file_error"],
            "level": "DEBUG",
            "propagate": False,
        },
        "api": {
            "handlers": ["console", "file_info", "file_error"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file_info", "file_error"],
        "level": "INFO",
    },
}
