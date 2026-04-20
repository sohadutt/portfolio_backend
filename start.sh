#!/usr/bin/env bash
set -o errexit

cd "$(dirname "$0")/backend"

# 1. Run build-related tasks
uv run manage.py collectstatic --noinput

# 2. Start Celery in the BACKGROUND (Notice the & at the very end!)
uv run celery -A config worker --loglevel=info --pool=solo &

# 3. Start Gunicorn in the foreground
exec uv run gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-10000}"