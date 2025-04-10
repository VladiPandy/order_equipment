#!/bin/bash

# Загрузка переменных окружения
#set -a
#source /.env
#set +a

echo "Waiting for postgres..."

# Ждем пока база данных станет доступной
until pg_isready -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER}; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL started"

echo "Running migrations..."
python3 manage.py migrate

echo "Creating superuser (if not exists)..."
# Если суперпользователь уже существует, команда выдаст ошибку, которую можно проигнорировать.
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME} \
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL} \
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} \
python3 manage.py createsuperuser --noinput || echo "Superuser already exists or creation skipped"

echo "Starting Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000