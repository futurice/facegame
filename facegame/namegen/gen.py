from django.conf import settings
from django.core.cache import cache

import random
import os.path

NAMES = {
'first_name': 'finnish_names_men',
'last_name': 'last_names',}

def get_key(name):
    return 'names-{0}'.format(name)

def get_names(name):
    filename = NAMES[name]
    KEY = get_key(filename)
    result = cache.get(KEY)
    if result is None:
        path = os.path.join(settings.PROJECT_ROOT, 'facegame/namegen', filename)
        result = open(path).read()
        result = [k.strip() for k in result.split("\n") if k.strip()]
        cache.set(KEY, result)
    return result

def get_rnd(name):
    names = get_names(name)
    return random.choice(names)

def get_random_name():
    first_name = get_rnd('first_name')
    last_name = get_rnd('last_name')
    username = first_name[0:2] + last_name[0:3]
    return ("%s" % username.lower(), "%s %s" % (first_name, last_name))
