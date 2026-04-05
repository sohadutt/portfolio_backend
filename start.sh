#!/usr/bin/env bash
set -o errexit

python manage.py migrate

# Use pool=solo to force Celery to run in the main thread without spawning sub-processes.
# This severely limits throughput (it can only process 1 task at a time), 
# but it drastically reduces memory consumption.
celery -A backend worker --loglevel=info --pool=solo &

gunicorn backend.wsgi:application