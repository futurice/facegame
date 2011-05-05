#!/bin/sh
#

PROJDIR=$HOME/facegame
PIDFILE="$PROJDIR/facegame.pid"
SOCKET="$PROJDIR/facegame.sock"
#OUTLOG="$PROJDIR/logs/access.log"
#ERRLOG="$PROJDIR/logs/error.log"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

/usr/bin/env - \
  PYTHONPATH="../python:.." \
  ./manage.py runfcgi --settings=facegame.settings socket=$SOCKET pidfile=$PIDFILE workdir=$PROJDIR

chmod a+w $SOCKET
