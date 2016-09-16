
import os
import sys

path = "/opt/app/facegame/"

if not path in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "facegame.settings.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
