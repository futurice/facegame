#!/bin/bash
./manage.py migrate --noinput
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf