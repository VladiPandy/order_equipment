#!/bin/sh

echo "Waiting for postgres..."

#while ! nc -z $DB_HOST $DB_PORT; do
sleep 0.5
#done

echo "PostgreSQL started"

echo "Running migrations..."
python3 manage.py migrate

echo "Creating superuser (if not exists)..."
# Если суперпользователь уже существует, команда выдаст ошибку, которую можно проигнорировать.
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@example.com \
DJANGO_SUPERUSER_PASSWORD=adminpassword \
python3 manage.py createsuperuser --noinput || echo "Superuser already exists or creation skipped"

echo "Starting Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000