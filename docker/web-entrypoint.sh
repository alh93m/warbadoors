#!/bin/sh
set -e

# Simple entrypoint for container. By default do not auto-migrate in production.
echo "Starting web container (DJANGO_ENV=${DJANGO_ENV:-development})"

if [ "${AUTO_MIGRATE}" = "true" ]; then
  echo "AUTO_MIGRATE is true — running migrations"
  python manage.py migrate --noinput
else
  echo "AUTO_MIGRATE not enabled — skipping automatic migrations"
fi

echo "Collecting static files"
python manage.py collectstatic --noinput

exec gunicorn warba_doors.wsgi:application --bind 0.0.0.0:8000 --workers 3
