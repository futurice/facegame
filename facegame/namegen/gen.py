""" Generates random name from provided datafiles """

from django.conf import settings
from django.core.cache import cache

import random
import os.path

NAMES = {
'first_name': 'finnish_names_men',
'last_name': 'last_names',}

def get_key(filename):
    """ Returns cache key for given filename """
    return 'names-{0}'.format(filename)

def get_names(name):
    """ Returns list of names """
    filename = NAMES[name]
    file_cache = get_key(filename)
    result = cache.get(file_cache)
    if result is None:
        path = os.path.join(settings.PROJECT_ROOT, 'facegame/namegen', filename)
        result = open(path).read()
        result = [k.strip() for k in result.split("\n") if k.strip()]
        cache.set(file_cache, result)
    return result

def get_rnd(component):
    """ Returns random first or last name. Component should be either
        'first_name' or 'last_name' """
    names = get_names(component)
    return random.choice(names)

def get_random_name():
    """ Returns random full name with relevant username """
    first_name = get_rnd('first_name')
    last_name = get_rnd('last_name')
    username = first_name[0:2] + last_name[0:6]
    return ("%s" % username.lower(), "%s %s" % (first_name, last_name))
