FROM postgres:15

# Установка необходимых пакетов для сборки pg_cron
RUN apt-get update && apt-get install -y \
    postgresql-server-dev-15 \
    make \
    gcc \
    git \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Установка pg_cron
RUN git clone https://github.com/citusdata/pg_cron.git \
    && cd pg_cron \
    && make \
    && make install

# Добавляем pg_cron в shared_preload_libraries
RUN echo "shared_preload_libraries = 'pg_cron'" >> /usr/share/postgresql/postgresql.conf.sample \
    && echo "cron.database_name = '${DB_NAME}'" >> /usr/share/postgresql/postgresql.conf.sample \
    && echo "cron.host = 'localhost'" >> /usr/share/postgresql/postgresql.conf.sample
# Копируем скрипты
COPY create_schema.sql /docker-entrypoint-initdb.d/create_schema.sql
COPY init_backup.sql /docker-entrypoint-initdb.d/init_backup.sql
COPY backup.sh /var/lib/postgresql/backup.sh
COPY restore.sh /docker-entrypoint-initdb.d/restore.sh

# Устанавливаем права на скрипты
RUN chmod 777 /var/lib/postgresql/backup.sh \
    && chmod 777 /docker-entrypoint-initdb.d/restore.sh \
    && mkdir -p /var/lib/postgresql/backups \
    && chown -R postgres:postgres /var/lib/postgresql/backups \
    && chown postgres:postgres /var/lib/postgresql/backup.sh

# Настройка cron для ежедневного бэкапа в 2:00
RUN echo "20 * * * * postgres /var/lib/postgresql/backup.sh >> /var/log/postgresql/cron.log 2>&1" > /etc/cron.d/postgres-backup \
    && chmod 777 /etc/cron.d/postgres-backup \
    && chmod 777 /var/lib/postgresql/backup.sh \
    && touch /var/log/postgresql/cron.log \
    && chown postgres:postgres /var/log/postgresql/cron.log


