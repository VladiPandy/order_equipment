#!/bin/bash
#set -a
#source ../.env # Укажите правильный путь к вашему .env файлу
#set +a

# Настройки
BACKUP_DIR="/var/lib/postgresql/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"

# Создаем директорию для бэкапов, если её нет
mkdir -p $BACKUP_DIR

# Выполняем бэкап
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_FILE

# Удаляем старые бэкапы (оставляем только последние 7)
find $BACKUP_DIR -name "${DB_NAME}_*.sql.gz" -type f -mtime +7 -delete

# Логируем результат
echo "Backup completed: $BACKUP_FILE" >> /var/log/postgresql/backup.log 