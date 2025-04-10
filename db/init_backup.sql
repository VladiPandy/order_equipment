-- Создаем функцию для выполнения бэкапа
CREATE OR REPLACE FUNCTION perform_backup()
RETURNS void AS $$
BEGIN
    -- Выполняем скрипт бэкапа
    PERFORM dblink_exec('dbname=' || current_database(), 
        '\! /var/lib/postgresql/backup.sh');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Настраиваем периодическое выполнение бэкапа
-- Бэкап будет выполняться каждый день в 2:00
SELECT cron.schedule('0 2 * * *', 'SELECT perform_backup()');

-- Создаем таблицу для хранения информации о бэкапах
CREATE TABLE IF NOT EXISTS backup_history (
    id SERIAL PRIMARY KEY,
    backup_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    backup_file TEXT,
    status TEXT
); 