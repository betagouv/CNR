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

HOST_URL = os.getenv("HOST_URL", "127.0.0.1, localhost")

ALLOWED_HOSTS = (
    HOST_URL.replace(" ", "").split(",")
)

INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition
INSTALLED_APPS = [
    "storages",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail.search",
    "wagtail",
    "taggit",
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
    "cms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_referrer_policy.middleware.ReferrerPolicyMiddleware",
    "csp.middleware.CSPMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]


# Add debug toolbar
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"] + ALLOWED_HOSTS


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
CSP_FRAME_SRC = ["*.youtube.com", "*.mtcaptcha.com", "*.facebook.com", "*.vimeo.com", "datawrapper.dwcdn.net", "form.typeform.com"]
CSP_IMG_SRC = [
    "'self'",
    "data:",
    "localhost:" + runserver.default_port,
    "axeptio.imgix.net",
    "*.google.com",
    "*.gstatic.com",
    "*.facebook.com",
    "*.google.fr",
    "cellar-c2.services.clever-cloud.com",
]
CSP_STYLE_SRC = [
    "'self'",
    "'unsafe-hashes'",
    "'sha256-d//Lck7pNf/OY9MPfGYaIOTmqjEzvwlSukK3UObI08A='",  # inject-svg.js de django-dsfr
    "'sha256-Eyt3MCqJJqqqUJzUlVq9BLYX+kVGQZVLpJ4toZz4mb8='",  # inject-svg.js de django-dsfr
    "'sha256-Xhd5+zYamb/dMdyIkYwXmzaXokrsMrINTdCsO/s+Hcc='",  # inject style inline for homepage cover (old)
    "'sha256-dDZkVrIJy1Xyahb04E1npPS7ONJw3g8949x7gAc/kEY='",  # inject style inline for homepage cover
    "'sha256-R2Vkrx5FLpmMY0750ljuQem15/f/bIrrGl+TXyzeETo='",  # mtcaptcha
    "'sha256-8kPOCl/iIr6YgWLvLnIRMrYnCJHOzs6WNYAedT41SM8='",  # mtcaptcha
    "'sha256-2Go/yMtz4sEcAbw1TnjkjLz983Zxq7frCShdJs2OobM='",  # mtcaptcha
    "'sha256-g6zf946PtVM63bZ+fe9QUc3hDXp5BMl6OBmAlKhKV60='",  # mtcaptcha
    "'sha256-zqo/Gf4mmbgvoqPGTNSkHYfibgllewm/seDhWyooOOk='",  # mtcaptcha
    "'sha256-FVE4UqDzJ5GzKFQlZqU4Zq3EAxxb/T0hpPQU9k6uwkA='",  # mtcaptcha
    "'sha256-/68szNaQXdlDug09n2c6rD/J5VWzEfkXCRsVxk+Bc7s='",  # datawrapper
    "'sha256-AthIs6YNuVjwfheHgESE8WAfJ61fXMZXX7s/UwRV5Dg='",  # typeform nps
    "embed.typeform.com",  # typeform nps
]
CSP_SCRIPT_SRC = [
    "'self'",
    "'sha256-bniFC3kd4JwCYRuTuxW9AjUYecKEuyTLJ+5NH6TJBWE='",  # matomo
    "stats.conseil-refondation.fr",  # matomo
    "service.mtcaptcha.com",
    "service2.mtcaptcha.com",
    "'sha256-7I5+oMehC+KBd+/dcrEMSPXSBUa0CSjemqYTkGftfeo='",  # MTCaptcha staging public key
    "'sha256-GWPBP28u9s4u/wssaakyNjieplIhhXg1ExHLViqsF6s='",  # MTCaptcha production public key
    "'sha256-1neh+DsrMKevQd7CmK4xkhFjYHtrpaiR8ncbjLw/w5E='",  # cookies handler
    "connect.facebook.net",
    "static.axept.io",
    "www.googletagmanager.com",
    "www.googleadservices.com",
    "googleads.g.doubleclick.net",
    "embed.typeform.com",  # typeform nps
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
    "form.typeform.com",
]

# https://django-csp.readthedocs.io/en/latest/configuration.html?highlight=CSP_EXCLUDE_URL_PREFIXES#other-settings
CSP_EXCLUDE_URL_PREFIXES = ("/cms-admin/",)

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
if DEBUG:
    conn_max_age = 0
else:
    conn_max_age = int(os.getenv("DATABASE_MAX_CONN_AGE", 0))

if postgres_url:
    environment_info = turn_psql_url_into_param(postgres_url)
    DATABASES = {
        "default": {
            "CONN_MAX_AGE": conn_max_age,
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
            "CONN_MAX_AGE": conn_max_age,
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

# S3 uploads
# ------------------------------------------------------------------------------

AWS_S3_ACCESS_KEY_ID = os.getenv("S3_KEY_ID", "123")
AWS_S3_SECRET_ACCESS_KEY = os.getenv("S3_KEY_SECRET", "secret")
AWS_S3_ENDPOINT_URL = (
    f"{os.getenv('S3_PROTOCOL', 'https')}://{os.getenv('S3_HOST', 'set-var-env.com/')}"
)
AWS_STORAGE_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "set-bucket-name")
AWS_S3_STORAGE_BUCKET_REGION = os.getenv("S3_BUCKET_REGION", "fr")

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = f"https://{AWS_S3_ENDPOINT_URL}/"  # noqa

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Wagtail settings
# https://docs.wagtail.org/en/stable/reference/settings.html

WAGTAIL_SITE_NAME = "Conseil National de la Refondation"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = f"{os.getenv('HOST_PROTO', 'https')}://{HOST_URL[-1]}"

# Disable Gravatar service
WAGTAIL_GRAVATAR_PROVIDER_URL = None

WAGTAIL_RICHTEXT_FIELD_FEATURES = [
    "h2",
    "h3",
    "h4",
    "bold",
    "italic",
    "link",
    "document-link",
    "image",
    "embed",
]

WAGTAILEMBEDS_RESPONSIVE_HTML = True
WAGTAIL_MODERATION_ENABLED = False
