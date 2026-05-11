#!/usr/bin/env bash
set -o errexit

cd "$(dirname "$0")/backend"

echo "Collecting static files..."
uv run manage.py collectstatic --noinput
echo "Starting Celery worker..."
uv run celery -A config worker --loglevel=info --pool=solo &
echo "Starting Gunicorn..."
exec uv run gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-10000}"