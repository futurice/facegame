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
MEDIA_URL = '/facegame-static/'

URLS_BASE = '/facegame/'
