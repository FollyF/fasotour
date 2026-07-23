#!/bin/sh
set -e

python manage.py collectstatic --noinput
exec gunicorn application_web.wsgi:application --bind 0.0.0.0:8000