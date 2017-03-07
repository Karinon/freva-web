"""
This is your project's main settings file that can be committed to your
repo. If you need to override a setting locally, use local.py
"""

import os
import logging

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

import django.utils

def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

LOGIN_URL = '/?login_required=1'

# temporary directory for tailed scheduler files
TAIL_TMP_DIR = '/tmp/tail_offset/'

# Your project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../")

SUPPORTED_NONLOCALES = ['media', 'admin', 'static']

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Defines the views served for root URLs.
ROOT_URLCONF = 'django_evaluation.urls'

# Application definition
INSTALLED_APPS = (
    # Django contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.syndication',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',

    # Third-party apps, patches, fixes
#    'debug_toolbar',
    'compressor',
    'bootstrap3',
    'datatableview',
    'webpack_loader',
    'rest_framework',
#    'debug_toolbar_user_panel',

    'base',
    'plugins',
    'history',
    'solr',
    'externaluser',
)

# Place bcrypt first in the list, so it will be the default password hashing
# mechanism
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# Sessions
#
# By default, be at least somewhat secure with our session cookies.
SESSION_COOKIE_HTTPONLY = True

# Set this to true if you are using https
SESSION_COOKIE_SECURE = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.example.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.example.com/static/"
STATIC_URL = '/static/'

# URL for preview files
PREVIEW_URL = STATIC_URL + 'preview/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#    ('preview', '/home/freva/ral-ces/misc4freva/db4freva/preview/'),
    os.path.join(PROJECT_ROOT, 'assets')
)

print os.path.join(PROJECT_ROOT, 'assets')

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'
# TIME_ZONE = 'Europe/Berlin'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django_evaluation.middelwares.GlobalUserMiddleware',
    'django_evaluation.middelwares.ReloadPluginsMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
]

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


#DEBUG_TOOLBAR_PATCH_SETTINGS = False

def custom_show_toolbar(request):
    """ Only show the debug toolbar to users with the superuser flag. """
    return False#request.user.is_superuser


#DEBUG_TOOLBAR_CONFIG = {
#    'INTERCEPT_REDIRECTS': False,
#    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
#    'HIDE_DJANGO_SQL': True,
#    'TAG': 'body',
#    'SHOW_TEMPLATE_CONTEXT': True,
#    'ENABLE_STACKTRACES': True,
#}

#DEBUG_TOOLBAR_PANELS = (
#    'debug_toolbar.panels.versions.VersionsPanel',
#    'debug_toolbar.panels.timer.TimerPanel',
#    'debug_toolbar.panels.settings.SettingsPanel',
#    'debug_toolbar.panels.headers.HeadersPanel',
#    'debug_toolbar.panels.request.RequestPanel',
#    'debug_toolbar.panels.sql.SQLPanel',
#    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#    'debug_toolbar.panels.templates.TemplatesPanel',
#    'debug_toolbar.panels.cache.CachePanel',
#    'debug_toolbar.panels.signals.SignalsPanel',
#    'debug_toolbar.panels.logging.LoggingPanel',
#    'debug_toolbar.panels.redirects.RedirectsPanel', 
#)

FILE_UPLOAD_PERMISSIONS = 0664

# The WSGI Application to use for runserver
WSGI_APPLICATION = 'django_evaluation.wsgi.application'

INTERNAL_IPS = ('127.0.0.1')

SERVER_EMAIL = "miklip@met.fu-berlin.de"
DEFAULT_FROM_EMAIL = "miklip@met.fu-berlin.de"
SYSTEM_EMAIL_PREFIX = "[django_evaluation]"

EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='miklip.integration@gmail.com'
EMAIL_HOST_PASSWORD='1nt3gr@tion'
EMAIL_USE_TLS=True
EMAIL_PORT=587

## Log settings

LOG_LEVEL = logging.INFO
HAS_SYSLOG = True
SYSLOG_TAG = "http_app_django_evaluation"  # Make this unique to your project.

SECRET_KEY = 'hj1bkzobng0ck@0&%t509*1ki$#)i5y+i0)&=7zv@amu8pm5*t'

# Recipients of traceback emails and other notifications.
ADMINS = (
    ('Sebastian Illing', 'sebastian.illing@met.fu-berlin.de'),
    ('Christopher Kadow','christopher.kadow@met.fu-berlin.de'),
)
MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
DEBUG = TEMPLATE_DEBUG = False
DEV = False

# SECURITY WARNING: keep the secret key used in production secret!
# Hardcoded values can leak through source control. Consider loading
# the secret key from an environment variable or a file instead.
SECRET_KEY = 'hj1bkzobng0ck@0&%t509*1ki$#)i5y+i0)&=7zv@amu8pm5*t'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'simple_mail': {
            'format': 'Sent: %(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console_mail':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple_mail'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_false'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins', 'console_mail'],
            'propagate': False,
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['mail_admins', 'console_mail'],
            'level': 'ERROR',
            'propagate': True,
            'level': 'INFO',
        },

    }
}

INTERNAL_IPS = ('127.0.0.1')

# path to the site packages used:
VENV_PYTHON_DIR = '/usr/local/ve_py/bin/python'

# Restrictions for the data browser
SOLR_RESTRICTIONS = {'project':['cmip5', 'cordex', 'observations', 'reanalysis', 'baseline0', 'baseline1', 'prototype', 'example-user']}
EMAIL_RESTRICTIONS = ['b324031', 'b324057','u290038']


# filter for user numbers
USERNAME_FILTER='[a-z]\d{6,6}'
USERNAME_REPLACE='*****'


# send an email to the admins whenever a guest logs-in
SEND_MAIL_AT_GUEST_LOGIN = True

# result to show at guest tour
GUEST_TOUR_RESULT = 17508

# Django rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication'
    ]
}
