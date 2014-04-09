from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
import os, re, subprocess
import json
import requests

"""
minify all templates/js folders files and save to a file
"""
STATIC_DIR = 'static'

def stripcomments(text):
    return re.sub('// .*?\n|/\*.*?\*/', '', text, re.S)

def process_js_folders(BASEPATH, folders):
    print "JS folders", BASEPATH, folders
    tpl = {}
    for folder in folders:
        try:
            files = [k for k in os.listdir(BASEPATH + folder) if '.html' in k]
        except OSError, e:
            print e
            continue
        for k in files:
            name = k.split('.')[0]
            data = open(BASEPATH + folder + k).read()
            data = stripcomments(data)
            tpl[name] = data
    return tpl

def jstpl(folders=[], check=['templates/js',], filename='js/gen/custom_tpl_file.js'):
    """
    jstpl(
     folders=['/inventory/common/static/'],
     check=['templates/js/,'templates/js/report/'],
     filename='/js/gen/custom_tpl_file.js',
     )
    Output is written to first provided folder.
    """
    tpl = {}
    for folder in folders:
        # ensure dir exists
        command = 'mkdir -p {0}'.format(settings.PROJECT_ROOT + folder)
        output = subprocess.check_output(command.split())
        # fetch JS templates
        tpl.update(process_js_folders(settings.PROJECT_ROOT + folder, check))

    target = '{0}{1}'.format(settings.PROJECT_ROOT, filename)
    f = open(target, 'w')
    output = "var q={}; q.tplfile = %s;"%(json.dumps(tpl))
    f.write(output)
    print "jstpl(): %s" % target

def baseurl():
    pass

def contenttype_js():
    KEY = 'contenttypes'
    data = cache.get(KEY)
    if not data:
        data = requests.get(reverse('contenttype-list'))
        cache.set(KEY, data, 3600)
    return data

if __name__ == "__main__":
    jstpl()

