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

uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload