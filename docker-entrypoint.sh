#!/bin/sh
set -eu

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Loading the educational movie catalog..."
python manage.py seed_movies

echo "Ensuring the optional educational superuser..."
python manage.py ensure_superuser

exec "$@"
