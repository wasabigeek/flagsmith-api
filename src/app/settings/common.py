"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import warnings
import uuid
import requests
import sys

from corsheaders.defaults import default_headers

from app.utils import secret_key_gen

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/


if 'DJANGO_SECRET_KEY' not in os.environ:
    secret_key_gen()

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

HOSTED_SEATS_LIMIT = int(os.environ.get('HOSTED_SEATS_LIMIT', 0))

# Google Analytics Configuration
GOOGLE_ANALYTICS_KEY = os.environ.get('GOOGLE_ANALYTICS_KEY', '')
GOOGLE_SERVICE_ACCOUNT = os.environ.get('GOOGLE_SERVICE_ACCOUNT')
if not GOOGLE_SERVICE_ACCOUNT:
    warnings.warn("GOOGLE_SERVICE_ACCOUNT not configured, getting organisation usage will not work")
GA_TABLE_ID = os.environ.get('GA_TABLE_ID')
if not GA_TABLE_ID:
    warnings.warn("GA_TABLE_ID not configured, getting organisation usage will not work")

if 'DJANGO_ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split(',')
else:
    ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1',]

# In order to run a load balanced solution, we need to whitelist the internal ip
try:
    internal_ip = requests.get('http://instance-data/latest/meta-data/local-ipv4').text
except requests.exceptions.ConnectionError:
    pass
else:
    ALLOWED_HOSTS.append(internal_ip)
del requests

if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'api',
    'corsheaders',
    'users',
    'organisations',
    'projects',
    'environments',
    'features',
    'segments',
    'e2etests',
    'simple_history',
    'debug_toolbar',
    'drf_yasg',
    'audit',
    'permissions',

    # health check plugins
    'health_check',
    'health_check.db',
]

if GOOGLE_ANALYTICS_KEY:
    INSTALLED_APPS.append('analytics')

SITE_ID = 1

# Initialise empty databases dict to be populated in environment settings
DATABASES = {}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'PAGE_SIZE': 10,
    'UNICODE_JSON': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination'
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.UserRegisterSerializer'
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserFullSerializer'
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

if GOOGLE_ANALYTICS_KEY:
    MIDDLEWARE.append('analytics.middleware.GoogleAnalyticsMiddleware')

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, '../../static/')

# CORS settings

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + (
    'X-Environment-Key',
    'X-E2E-Test-Auth-Token'
)

DEFAULT_FROM_EMAIL = "noreply@bullet-train.io"
EMAIL_CONFIGURATION = {
    # Invitations with name is anticipated to take two arguments. The persons name and the
    # organisation name they are invited to.
    'INVITE_SUBJECT_WITH_NAME': '%s has invited you to join the organisation \'%s\' on Bullet '
                                'Train',
    # Invitations without a name is anticipated to take one arguments. The organisation name they
    # are invited to.
    'INVITE_SUBJECT_WITHOUT_NAME': 'You have been invited to join the organisation \'%s\' on '
                                   'Bullet Train',
    # The email address invitations will be sent from.
    'INVITE_FROM_EMAIL': 'noreply@bullettrain.com',

}

# Used on init to create admin user for the site, update accordingly before hitting /auth/init
ALLOW_ADMIN_INITIATION_VIA_URL = True
ADMIN_EMAIL = "admin@example.com"
ADMIN_INITIAL_PASSWORD = "password"

AUTH_USER_MODEL = 'users.FFAdminUser'

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'  # TODO: configure email verification

# SendGrid
EMAIL_BACKEND = 'sgbackend.SendGridBackend'
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
if not SENDGRID_API_KEY:
    warnings.warn(
        "`SENDGRID_API_KEY` has not been configured. You will not receive emails.")

SWAGGER_SETTINGS = {
    'SHOW_REQUEST_HEADERS': True,
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
}

LOGIN_URL = "/admin/login/"
LOGOUT_URL = "/admin/logout/"

# Email associated with user that is used by front end for end to end testing purposes
FE_E2E_TEST_USER_EMAIL = "nightwatch@solidstategroup.com"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Chargebee
ENABLE_CHARGEBEE = os.environ.get('ENABLE_CHARGEBEE', False)
CHARGEBEE_API_KEY = os.environ.get('CHARGEBEE_API_KEY')
CHARGEBEE_SITE = os.environ.get('CHARGEBEE_SITE')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_format': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_format',
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console']
        },
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
}

CACHE_FLAGS_SECONDS = int(os.environ.get('CACHE_FLAGS_SECONDS', 0))
FLAGS_CACHE_LOCATION = 'environment-flags'
ENVIRONMENT_CACHE_LOCATION = 'environment-objects'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
    ENVIRONMENT_CACHE_LOCATION: {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ENVIRONMENT_CACHE_LOCATION
    },
    FLAGS_CACHE_LOCATION: {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': FLAGS_CACHE_LOCATION,
    }
}