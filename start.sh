#!/usr/bin/env bash
set -o errexit

cd "$(dirname "$0")/backend"

python manage.py migrate

# Use pool=solo to force Celery to run in the main thread without spawning sub-processes.
# This severely limits throughput (it can only process 1 task at a time), 
# but it drastically reduces memory consumption.
celery -A config worker --loglevel=info --pool=solo &

exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-10000}"
