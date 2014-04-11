from settings import *

ADMINS = (
    ('Jussi Vaihia', 'jussi.vaihia@futurice.com'),
)
DEBUG = False
TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtpgw.futurice.com"
EMAIL_PORT = 25

STATIC_URL = '/facegame-static/'
MEDIA_URL = '/facegame-media/'

# PROJECT_ROOT -> DEPLOY_ROOT
MEDIA_ROOT = os.path.join(DEPLOY_ROOT, 'media') + os.sep
STATIC_ROOT = os.path.join(DEPLOY_ROOT, 'static') + os.sep
DATABASES['default']['NAME'] = os.path.abspath(os.path.join(DEPLOY_ROOT, 'sqlite.db')),

URLS_BASE = '/facegame/'
