import django.conf.global_settings as DEFAULT_SETTINGS
import os, hashlib, datetime, copy

PACKAGE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROJECT_ROOT = os.path.normpath(PACKAGE_ROOT)
DEPLOY_ROOT = PROJECT_ROOT

FUM_API_URL = os.getenv('FUM_API_URL', '')
FUM_API_TOKEN = os.getenv('FUM_API_TOKEN', '')

THUMB_SALT = ''

DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
FAKE_LOGIN = os.getenv('DEBUG', 'false').lower() == 'true'

USER_DATA = '{PROJECT_ROOT}/test_data.json'.format(**locals())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'facegame'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

ALLOWED_HOSTS = ['*']
TIME_ZONE = 'Europe/Helsinki'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = '/opt/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/opt/static/'
STATIC_URL = '/static/'

SECRET_KEY = os.getenv('SECRET_KEY', '')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 86400,
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
TEMPLATE_LOADERS = DEFAULT_SETTINGS.TEMPLATE_LOADERS
MIDDLEWARE_CLASSES = (
    'facegame.middleware.SetUserMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'facegame.middleware.CustomHeaderMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = DEFAULT_SETTINGS.AUTHENTICATION_BACKENDS + (
    'django.contrib.auth.backends.RemoteUserBackend',
)
ROOT_URLCONF = 'facegame.urls'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'facegame/templates/'),
)
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS  = (
    ('facegame.common.context_processors.settings_to_context',
    'django.core.context_processors.request',
    )+TEMPLATE_CONTEXT_PROCESSORS)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'django_extensions',
    'django_js_utils',
    'facegame.common',
    'facegame.faceguessing',
    'facegame.nameguessing',
)
AUTH_USER_MODEL = 'faceguessing.Player'

SENTRY_TESTING = True
SENTRY_KEY = ''
SENTRY_SERVERS = []

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'project':{
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

URLS_JS_GENERATED_FILE = 'facegame/common/static/js/gen/dutils.conf.urls.js'
URLS_JS_TO_EXPOSE = [
'api/',
'',
]
URLS_EXCLUDE_PATTERN = ['.(?P<format>[a-z0-9]+)','.(?P<format>+)','__debug__','admin',]
URLS_BASE = ''
URLS_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Groups, use a small pool for development
USER_GROUPS = ['helsinki', 'tampere', 'berlin', 'london', 'stockholm', 'munich', 'oslo']

try:
    from local_settings import *
except ImportError:
    pass
