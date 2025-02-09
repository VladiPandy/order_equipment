#!/bin/sh

echo "Waiting for postgres..."

#while ! nc -z $DB_HOST $DB_PORT; do
sleep 0.5
#done

echo "PostgreSQL started"

uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload