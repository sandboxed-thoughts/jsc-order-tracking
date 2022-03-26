"""
Django settings for tracker project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

import dj_database_url
from decouple import config

from .jazzmin_settings import JAZZMIN_SETTINGS, JAZZMIN_UI_TWEAKS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "phonenumber_field",
    "localflavor",
    "simple_history",
    "sass_processor",
    # project apps
    "jazzmin",
    "config.apps.ProjectAdminConfig",  # replaces 'django.contrib.admin'
    "apps.accounts",  # custom user model
    "apps.clients",
    "apps.concrete",
    "apps.core",
    "apps.gravel",
    "apps.orders",
    "apps.schedules",
    "apps.sites",
    "apps.suppliers",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = config("ROOT_URLCONF", default="config.urls")

INTERNAL_IPS = ["127.0.0.1"]

WSGI_APPLICATION = config("WSGI_APP", default="config.wsgi.application")

X_FRAME_OPTIONS = config("X_FRAME_OPTIONS", default="SAMEORIGIN")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.parent / "templates",
        ],
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

# Database - https://github.com/jacobian/dj-database-url
DATABASES = {"default": dj_database_url.config(default=config("DATABASE_URL"))}


# User model
AUTH_USER_MODEL = config("USER_MODEL")

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_URL = "/logout"

LOGOUT_REDIRECT_URL = LOGIN_URL

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = config("LANG_CODE", default="en-us")

TIME_ZONE = config("TIME_ZONE", default="America/New_York")

USE_I18N = config("I18N", cast=bool, default=True)

USE_TZ = config("USE_TZ", cast=bool, default=True)

PHONENUMBER_DB_FORMAT = config("PHONENUMBER_DB_FORMAT", default="E164")

PHONENUMBER_DEFAULT_REGION = config("PHONENUMBER_DEFAULT_REGION", default="US")

PHONENUMBER_DEFAULT_FORMAT = config("PHONENUMBER_DEFAULT_FORMAT", default="NATIONAL")

# Static files (CSS, JavaScript, Images)

STATIC_URL = config("STATIC_URL", default="/static/")

STATIC_ROOT = config("STATIC_ROOT")

STATICFILES_DIRS = [
    BASE_DIR.parent / "static",
    BASE_DIR.parent / "apps/core/static",
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]


# SASS
SASS_PRECISION = 8
SASS_OUTPUT_STYLE = "compact"
