from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import json
import slumber

def get_api():
    return slumber.API(settings.FUM_API_URL, auth=slumber.auth.TokenAuth(settings.FUM_API_TOKEN))

def to_json(data):
    return json.dumps(data, encoding='utf-8', cls=DjangoJSONEncoder, ensure_ascii=False, separators=(',',':'))
