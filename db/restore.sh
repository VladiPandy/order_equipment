#!/bin/bash
#set -a
#source ../.env # Укажите правильный путь к вашему .env файлу
#set +a

# Настройки
BACKUP_DIR="/var/lib/postgresql/backups"
LOG_FILE="/var/log/postgresql/restore.log"

# Функция для логирования
log_message() {
    local message="$1"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $message" | tee -a $LOG_FILE
}

# Проверяем наличие бэкапов
if [ -z "$(ls -A $BACKUP_DIR/*.sql.gz 2>/dev/null)" ]; then
    log_message "No backups found. Skipping restore."
    exit 0
fi

# Находим последний бэкап
LATEST_BACKUP=$(ls -t $BACKUP_DIR/*.sql.gz | head -1)
log_message "Found latest backup: $LATEST_BACKUP"

# Проверяем, существует ли база данных
if ! psql -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    log_message "Database $DB_NAME does not exist. Creating..."
    createdb -U $DB_USER $DB_NAME
fi

# Восстанавливаем из бэкапа
log_message "Starting restore from $LATEST_BACKUP..."
if gunzip -c $LATEST_BACKUP | psql -U $DB_USER -d $DB_NAME; then
    log_message "Restore completed successfully"
    # Записываем информацию о восстановлении
    psql -U $DB_USER -d $DB_NAME << EOF
    INSERT INTO backup_history (backup_file, status)
    VALUES ('$LATEST_BACKUP', 'restored');
EOF
else
    log_message "Restore failed"
    exit 1
fi 