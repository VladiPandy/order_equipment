#!/bin/bash
set -e

# Запускаем cron
gosu postgres cron

# Проверяем и восстанавливаем бэкап при первом запуске
gosu postgres /docker-entrypoint-initdb.d/restore.sh

# Запускаем PostgreSQL
exec docker-entrypoint.sh postgres