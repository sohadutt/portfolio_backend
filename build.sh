#!/usr/bin/env bash
set -o errexit

cd "$(dirname "$0")/backend"

echo "Installing UV and dependencies..."
pip install uv
uv sync

echo "Running database migrations..."
uv run manage.py collectstatic --noinput
uv run manage.py migrate