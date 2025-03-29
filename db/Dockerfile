FROM postgres:15

# Установка необходимых пакетов для сборки pg_cron
RUN apt-get update && apt-get install -y \
    postgresql-server-dev-15 \
    make \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка pg_cron
RUN git clone https://github.com/citusdata/pg_cron.git \
    && cd pg_cron \
    && export PATH=/usr/pgsql-16/bin:$PATH \
    && make \
    && sudo PATH=$PATH make install

# Добавляем pg_cron в shared_preload_libraries
RUN echo "shared_preload_libraries = 'pg_cron'" >> /usr/share/postgresql/postgresql.conf.sample \
    && echo "cron.database_name = 'DB_NAME'" >> /usr/share/postgresql/postgresql.conf.sample

COPY create_schema.sql /docker-entrypoint-initdb.d/create_schema.sql

