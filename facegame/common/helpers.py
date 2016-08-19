from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from requests.auth import AuthBase
import json
import simplejson
import slumber

class TokenAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = "Token {0}".format(self.token)
        print r.url
        return r

def get_api():
    if settings.FUM_API_URL:
        return slumber.API(settings.FUM_API_URL, auth=TokenAuth(settings.FUM_API_TOKEN))

def to_json(data):
    return json.dumps(data, encoding='utf-8', cls=DjangoJSONEncoder, ensure_ascii=False, separators=(',',':'))
