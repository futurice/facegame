from django.contrib.auth.middleware import RemoteUserMiddleware
from facegame.settings import settings
import os

#This middleware adds header REMOTE_USER with current REMOTE_USER from settings to every request.
#This is required when running app with uwsgi locally (with runserver this is unnecessary)
#In production, when FAKE_LOGIN=False, the REMOTE_USER header should be set by sso
class SetUserMiddleware():

    def process_request(self, request):
        if settings.FAKE_LOGIN:
            request.META['REMOTE_USER'] = settings.REMOTE_USER

class CustomHeaderMiddleware(RemoteUserMiddleware):
    header = os.getenv('REMOTE_USER_HEADER', 'REMOTE_USER')