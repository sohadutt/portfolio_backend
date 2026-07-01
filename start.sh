#!/usr/bin/env bash
set -o errexit

cd "$(dirname "$0")/backend"

echo "Starting Celery worker..."
uv run --no-sync celery -A config worker --loglevel=info --pool=solo --without-mingle --without-gossip &
echo "Starting Gunicorn..."
exec uv run --no-sync gunicorn config.wsgi:application --timeout 120 --bind "0.0.0.0:${PORT:-10000}"