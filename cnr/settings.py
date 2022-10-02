"""
Django settings for cnr project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

import sentry_sdk
from django.core.management.commands.runserver import Command as runserver
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

from cnr.utils.postgres import turn_psql_url_into_param

load_dotenv(".pg_service.conf")
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv("IS_DEBUG_ENABLED") == "True":
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = (
    os.getenv("HOST_URL", "127.0.0.1, localhost").replace(" ", "").split(",")
)

INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "widget_tweaks",
    "dsfr",
    "sass_processor",
    "public_website",
    "surveys",
    "behave_django",
    # "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_referrer_policy.middleware.ReferrerPolicyMiddleware",
    "csp.middleware.CSPMiddleware",
]

# Sentry
SENTRY_URL = os.getenv("SENTRY_URL", "")
if SENTRY_URL:
    sentry_sdk.init(
        dsn=SENTRY_URL,
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=float(os.getenv("SENTRY_SAMPLE_RATE", 0)),
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

# Security headers
SECURE_HSTS_SECONDS = 2592000
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
REFERRER_POLICY = "same-origin"
CSP_DEFAULT_SRC = ["'self'", "data:", "localhost:" + runserver.default_port]
CSP_FRAME_SRC = ["*.youtube.com", "*.mtcaptcha.com", "*.facebook.com"]
CSP_IMG_SRC = [
    "'self'",
    "data:",
    "localhost:" + runserver.default_port,
    "axeptio.imgix.net",
    "*.google.com",
    "*.gstatic.com",
    "*.facebook.com",
    "*.google.fr",
]
CSP_STYLE_SRC = [
    "'self'",
    "'unsafe-hashes'",
    "'sha256-d//Lck7pNf/OY9MPfGYaIOTmqjEzvwlSukK3UObI08A='",  # inject-svg.js de django-dsfr
    "'sha256-Eyt3MCqJJqqqUJzUlVq9BLYX+kVGQZVLpJ4toZz4mb8='",  # inject-svg.js de django-dsfr
    "'sha256-Xhd5+zYamb/dMdyIkYwXmzaXokrsMrINTdCsO/s+Hcc='",  # inject style inline for homepage cover
    "'sha256-R2Vkrx5FLpmMY0750ljuQem15/f/bIrrGl+TXyzeETo='",  # mtcaptcha
    "'sha256-8kPOCl/iIr6YgWLvLnIRMrYnCJHOzs6WNYAedT41SM8='",  # mtcaptcha
    "'sha256-2Go/yMtz4sEcAbw1TnjkjLz983Zxq7frCShdJs2OobM='",  # mtcaptcha
    "'sha256-2Go/yMtz4sEcAbw1TnjkjLz983Zxq7frCShdJs2OobM='",  # mtcaptcha
    "'sha256-g6zf946PtVM63bZ+fe9QUc3hDXp5BMl6OBmAlKhKV60='",  # mtcaptcha
    "'sha256-zqo/Gf4mmbgvoqPGTNSkHYfibgllewm/seDhWyooOOk='",  # mtcaptcha
    "'sha256-FVE4UqDzJ5GzKFQlZqU4Zq3EAxxb/T0hpPQU9k6uwkA='",  # mtcaptcha
    "'sha256-jPZyQpI7D4ke0fa/phXRncbbLQIiMkuCkTySdu4EzXc='",  # Axeptio
    "'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='",  # Axeptio
]
CSP_SCRIPT_SRC = [
    "'self'",
    "'sha256-bniFC3kd4JwCYRuTuxW9AjUYecKEuyTLJ+5NH6TJBWE='",  # matomo
    "stats.conseil-refondation.fr",  # matomo
    "service.mtcaptcha.com",
    "service2.mtcaptcha.com",
    "'sha256-jU1pIGvEWqCd3fkxyXEsy7NoGw0NZLsrWRt69jP8m6g='",  # MTCaptcha staging public key
    "'sha256-taOKAZWPEC2SOqviO83qxLRLXWLc7lk22f4uZzbNsxU='",  # MTCaptcha production public key
    "'sha256-Oa6BZnRhi/9APENlptbCGkRRDfZFnkgCefn2wen8cYM='",  # Axeptio
    "connect.facebook.net",
    "static.axept.io",
    "https://www.googletagmanager.com/gtag/js",
    "https://www.googleadservices.com/pagead/conversion_async.js",
    "googleads.g.doubleclick.net/",
]
CSP_CONNECT_SRC = [
    "connect.facebook.net",
    "*.facebook.com",
    "'self'",
    "stats.conseil-refondation.fr",
    "client.axept.io",
    "api.axept.io",
    "googletagmanager.com",
    "googleadservices.com",
    "googleads.g.doubleclick.net/",
]

ROOT_URLCONF = "cnr.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "dsfr/templates"),
            os.path.join(BASE_DIR, "templates"),
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

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "cnr.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

postgres_url = os.getenv("DATABASE_URL")
if postgres_url:
    environment_info = turn_psql_url_into_param(postgres_url)
    DATABASES = {
        "default": {
            "CONN_MAX_AGE": 60,
            "ENGINE": "django.db.backends.postgresql",
            "NAME": environment_info.get("db_name"),
            "USER": environment_info.get("db_user"),
            "PASSWORD": environment_info.get("db_password"),
            "HOST": environment_info.get("db_host"),
            "PORT": environment_info.get("db_port"),
        }
    }

    ssl_option = environment_info.get("sslmode")

else:
    DATABASES = {
        "default": {
            "CONN_MAX_AGE": 60,
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DATABASE_NAME"),
            "USER": os.getenv("DATABASE_USER"),
            "PASSWORD": os.getenv("DATABASE_PASSWORD"),
            "HOST": os.getenv("DATABASE_HOST"),
            "PORT": os.getenv("DATABASE_PORT"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "fr-FR"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True

# LANGUAGES = [
#     ("fr", gettext_noop("French")),
#     ("en", gettext_noop("English")),
# ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
]
# Django Sass
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "static/"
STATIC_ROOT = "staticfiles"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SEND_IN_BLUE_API_KEY = os.getenv("SEND_IN_BLUE_API_KEY")
SEND_IN_BLUE_LIST = int(os.getenv("SEND_IN_BLUE_LIST", 1))

MOCK_EXTERNAL_API = os.getenv("MOCK_EXTERNAL_API", "False")
MTCAPTCHA_PRIVATE_KEY = os.getenv("MTCAPTCHA_PRIVATE_KEY", "")
MTCAPTCHA_PUBLIC_KEY = os.getenv("MTCAPTCHA_PUBLIC_KEY", "")

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60

IS_WAIT_PAGE_ON = os.getenv("IS_WAIT_PAGE_ON", False)
