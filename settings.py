# Django settings for facegame project.
import os
import hashlib

# ---- FUM API settings
FUMAPI_CONNECTION = {
    'USER': 'facegame',
    'PASSWORD': 'G4HJ1vLdhA',
    'SERVERS': ['https://fum3.futurice.com/api/',],
    'FUMAPI_ROOT': '/facegame/',
}
FUMAPI_LOGFILE = 'access.log'

FUMAPI_CACHE = '/tmp/fumapicache_facegame/'
# ----

STATIC_ROOT = os.path.abspath("media")
STATIC_URL = '/static/'

ANONYMOUS_PIC = hashlib.md5(open("/home/facegame/facegame/media/images/anonymous.png").read()).hexdigest()

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
#    ('admin', 'admin@futurice.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'facegamedb',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Helsinki'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.abspath("media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')&$k692@_8z5d$3py^^9nddc5ln$3j0(8z%w98%23v=kuec25!'

#TEMPLATE_CONTEXT_PROCESSORS = (
#	'django.contrib.auth.context_processors.auth',
#	'django.core.context_processors.debug',
#	'django.core.context_processors.i18n',
#	'django.core.context_processors.media',
#	'django.contrib.messages.context_processors.messages',
#)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'intra-facegame'
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'facegame.urls'

TEMPLATE_DIRS = (
    "templates",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'faceguessing',
    'fumapi',
    'sentry.client',
    'django.contrib.admin',
)

SENTRY_TESTING = True
SENTRY_KEY = 'js52wjdsoisr78fgs1f0g415safg1'
SENTRY_REMOTE_URL = 'https://sentry.futurice.com/sentry/store/'
#SESSION_COOKIE_AGE = 1209600
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#FUM ---- Settings override for developpment
#try :
#	from env_settings import *
#except ImportError as e:
#	print "WARNING : settings for the development environment couldn't be imported because:", e
