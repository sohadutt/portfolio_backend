#!/usr/bin/env bash
set -o errexit

cd "$(dirname "$0")/backend"

echo "Installing UV and dependencies..."
pip install uv
uv sync

echo "Running database migrations..."
uv run manage.py collectstatic --noinput
uv run celery -A config worker --loglevel=info --pool=solo &
exec uv run gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-10000}"