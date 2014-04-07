import os
import site
from os.path import abspath, dirname, join
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "facegame.settings.prod")

site.addsitedir('/srv/www/facegame/venv/lib/python2.7/site-packages')
DJANGO_PROJECTDIR = abspath(join(dirname(__file__), '../..'))
ALLDIRS = [abspath(join(DJANGO_PROJECTDIR, '..')),]
site.addsitedir(abspath(join(DJANGO_PROJECTDIR, '')))
for directory in ALLDIRS:
    site.addsitedir(abspath(join(DJANGO_PROJECTDIR, directory)))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
