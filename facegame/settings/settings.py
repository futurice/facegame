import django.conf.global_settings as DEFAULT_SETTINGS

import os, hashlib, datetime, copy
import slumber

PACKAGE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROJECT_ROOT = os.path.normpath(PACKAGE_ROOT)
DEPLOYMENT_ROOT = PROJECT_ROOT

FUM_API_URL = 'https://api.fum.futurice.com/v1/'
FUM_API_TOKEN = '46eab140e97bd7594102a774de5921765e0db298'
API = slumber.API(FUM_API_URL, auth=slumber.auth.TokenAuth(FUM_API_TOKEN))

ANONYMOUS_PIC = hashlib.md5(open(os.path.join(PROJECT_ROOT, "media/images/anonymous.png")).read()).hexdigest()
ANONYMOUS_THUMB = hashlib.md5(open(os.path.join(PROJECT_ROOT, "media/images/anonymousthumb.jpg")).read()).hexdigest()
PATH_TO_FUTUPIC = "/var/www/intra.futurice.org/futupic/"

DEBUG = True
TEMPLATE_DEBUG = True
ADMINS = (
    ('Jussi Vaihia', 'jussi.vaihia@futurice.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '{PROJECT_ROOT}/sqlite.db'.format(**locals()),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = ['*']
TIME_ZONE = 'Europe/Helsinki'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = '{PROJECT_ROOT}/media/'.format(**locals())
MEDIA_URL = '/media/'

STATIC_ROOT = '{PROJECT_ROOT}/static/'.format(**locals())
STATIC_URL = '/static/'

SECRET_KEY = ')&$k692@_8z5d$3py^^9nddc5ln$3j0(8z%w98%23v=kuec25!'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
TEMPLATE_LOADERS = DEFAULT_SETTINGS.TEMPLATE_LOADERS
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = DEFAULT_SETTINGS.AUTHENTICATION_BACKENDS + (
    'django.contrib.auth.backends.RemoteUserBackend',
)
ROOT_URLCONF = 'facegame.urls'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates/'),
)
TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS
INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.admin',

        'django_extensions',
        'facegame.faceguessing',
        'facegame.nameguessing',
        )
IMAGEDIR = "/var/www/intra.futurice.org/futupic"
SENTRY_TESTING = True
SENTRY_KEY = 'js52wjdsoisr78fgs1f0g415safg1'
SENTRY_SERVERS = ['https://sentry.futurice.com/sentry/store/']

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
