from django.conf import settings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import datetime
import time, logging, subprocess, os

#from facegame.common.js_handle import jstpl
#from djangojsonmodel.convert import jsmodels

logging.basicConfig(level=logging.INFO)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "facegame.settings.settings")

INITIAL = 'INITIAL/WARMUP/REQUEST'
RUN_FOR = ['.js','.css','.less','.html','.yaml','WARMUP','urls.py',INITIAL]
BLACKLIST = [
'.git',
'dist/',
'node_modules/',
settings.MEDIA_ROOT.rstrip('/'),
settings.STATIC_ROOT.rstrip('/'),
'/gen/',
'.json',
]

def blacklisted(path):
    return any(black in path for black in BLACKLIST)

def runcmd(cmd):
    start = datetime.datetime.now()
    try:
        output = subprocess.check_output(cmd.split())
    except Exception, e:
        print e
    print " ran '{0}' in {1}".format( cmd, str((datetime.datetime.now()-start))[6:10])

LAST_RUN = datetime.datetime.now()
def is_time_to_run_again(interval=1):
    global LAST_RUN
    # TODO: check against *same* file; now skips changes if done against a different file...
    now = datetime.datetime.now()
    diff = (now-LAST_RUN).total_seconds()
    r = diff > interval
    if r:
        LAST_RUN = now
    return r

class CollectStaticHandler(FileSystemEventHandler):
    def prepare_system(self, event):
        if not blacklisted(event.src_path):
            start = datetime.datetime.now()
            if not is_time_to_run_again() and 'WARMUP' not in event.src_path:
                print " (( sleeping )) "
                return
            if any([k in event.src_path for k in RUN_FOR]):
                if not any(k in event.src_path for k in ['.html']):
                    runcmd('python manage.py js_urls')
                if any(k in event.src_path for k in ['.css','.js','templates/common/js', INITIAL]):
                    # TODO: use regex to match js/*.html
                    """
                    jstpl(folders=['/facegame/common/templates/'],
                         check=['common/js/',],
                         filename='/facegame/common/static/js/gen/custom_tpl_file.js',)
                    """
                runcmd('assetgen --profile dev assetgen.yaml --force')
                if not any(k in event.src_path for k in ['.html']):
                    runcmd('python manage.py collectstatic --link --noinput')
            print ":> ({0}s) {1}".format( str((datetime.datetime.now()-start))[6:10], event.src_path)
    def on_moved(self, event):
        what = 'directory' if event.is_directory else 'file'
        self.prepare_system(event)
    def on_created(self, event):
        what = 'directory' if event.is_directory else 'file'
        self.prepare_system(event)
    def on_deleted(self, event):
        what = 'directory' if event.is_directory else 'file'
        self.prepare_system(event)
    def on_modified(self, event):
        what = 'directory' if event.is_directory else 'file'
        self.prepare_system(event)

if __name__ == "__main__":
    print "Watcher Online."
    observer = Observer()
    observer.schedule(CollectStaticHandler(), path='.', recursive=True)

    # run once, to catchup on any changes while offline
    CollectStaticHandler().prepare_system( type('Event', (object,), {'src_path': INITIAL}) )

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


