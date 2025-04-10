SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Создаем расширение pg_cron
CREATE EXTENSION IF NOT EXISTS pg_cron;

CREATE TABLE IF NOT EXISTS public.projects_booking (
	id int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
	project_id uuid NOT NULL,
	date_booking date NOT NULL,
	analyse_id uuid NOT NULL,
	equipment_id uuid NOT NULL,
	executor_id uuid NOT NULL,
	count_analyses int4 NOT NULL,
	status varchar(254) NOT NULL,
	is_delete bool NULL,
	"comment" text NULL,
	CONSTRAINT projects_booking_id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.block_booking (
	id int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
	project_id uuid NOT NULL,
    booking_id int4 NULL,
	date_booking date NULL,
	analyse_id uuid NULL,
	equipment_id uuid NULL,
	executor_id uuid NULL,
	is_block bool NULL,
	write_timestamp timestamp NOT NULL DEFAULT now(),
	cookies_key uuid NOT NULL DEFAULT gen_random_uuid(),
	update_timestamp timestamp NULL,
	id_delete bool NULL DEFAULT false,
	CONSTRAINT block_booking_id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.feedback_task (
	booking_id int4 NOT NULL,
	question_1 bool NOT NULL DEFAULT True,
	question_2 bool NOT NULL DEFAULT True,
    question_3 bool NOT NULL DEFAULT True,
	CONSTRAINT feedback_booking_id PRIMARY KEY (booking_id)
);

-- Создаем функцию для обновления статуса
CREATE OR REPLACE FUNCTION public.update_booking_status()
RETURNS integer
LANGUAGE plpgsql
AS $$
DECLARE
    updated_count integer;
BEGIN
    -- Обновляем статус для всех записей, где статус 'Согласовано'
    UPDATE public.projects_booking
    SET status = 'Оценить'
    WHERE status = 'Выполнено'
    AND is_delete = false
    RETURNING COUNT(*) INTO updated_count;
    
    -- Логируем количество обновленных записей
    RAISE NOTICE 'Обновлено % записей', updated_count;
    
    RETURN updated_count;
END;
$$;  -- Закрытие долларовых кавычек

-- Добавляем комментарий к функции
COMMENT ON FUNCTION public.update_booking_status IS 'Обновляет статус бронирования с "Согласовано" на "Оценить" для записей текущего дня';

-- Создаем задачу, которая будет запускаться каждый день в 00:01
SELECT cron.schedule('update_booking_status', '5 0 * * *', $$
    SELECT public.update_booking_status();
$$);



CREATE OR REPLACE FUNCTION public.create_weekly_worker_status()
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    start_date DATE;
    end_date DATE;
    executor RECORD;
    current_week_period VARCHAR(50);  -- Переименованная переменная
BEGIN
    -- Определяем начало и конец недели через две недели от текущей даты
    start_date := date_trunc('week', CURRENT_DATE + INTERVAL '2 weeks');
    end_date := start_date + INTERVAL '6 days';
    -- Форматируем даты в строку для хранения в week_period
    current_week_period := to_char(start_date, 'DD.MM.YYYY') || '-' || to_char(end_date, 'DD.MM.YYYY');
    -- Проверяем, существуют ли записи на текущую неделю
    IF NOT EXISTS (
        SELECT 1
        FROM public.control_enter_workerweekstatus
        WHERE week_period = current_week_period
    ) THEN
        FOR executor IN SELECT id FROM public.executor LOOP
            INSERT INTO public.control_enter_workerweekstatus (
                id,
                created,
                modified,
                week_period,
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
                limit_executor,
                executor_id
            ) VALUES (
                uuid_generate_v4(),
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                current_week_period,  -- Используем переименованную переменную
                'Работает',  -- Пример статуса для понедельника
                'Работает',  -- Пример статуса для вторника
                'Работает',  -- Пример статуса для среды
                'Работает',  -- Пример статуса для четверга
                'Выходной',  -- Пример статуса для пятницы
                'Выходной',  -- Пример статуса для субботы
                'Выходной',  -- Пример статуса для воскресенья
                2,  -- Пример лимита исполнителей
                executor.id
            );
        END LOOP;
        RAISE NOTICE 'Созданы записи для недели с % до %', start_date, end_date;
    ELSE
        RAISE NOTICE 'Записи уже существуют для недели с % до %', start_date, end_date;
    END IF;
END;
$$;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

COMMENT ON FUNCTION public.create_weekly_worker_status IS 'Создает записи в таблице control_enter_workerweekstatus для недели через две недели от текущей даты, если они отсутствуют.';

SELECT cron.schedule('create_weekly_worker_status', '0 0 * * 1', $$ SELECT public.create_weekly_worker_status(); $$);



CREATE OR REPLACE FUNCTION public.create_weekly_working_day_status()
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
    start_date DATE;
    end_date DATE;
    current_week_period VARCHAR(50);
BEGIN
    -- Определяем начало и конец недели через две недели от текущей даты
    start_date := date_trunc('week', CURRENT_DATE + INTERVAL '2 weeks');
    end_date := start_date + INTERVAL '6 days';
    -- Форматируем даты в строку для хранения в week_period
    current_week_period := to_char(start_date, 'DD.MM.YYYY') || '-' || to_char(end_date, 'DD.MM.YYYY');
    -- Проверяем, существуют ли записи на текущую неделю
    IF NOT EXISTS (
        SELECT 1
        FROM public.control_enter_workingdayofweek
        WHERE week_period = current_week_period
    ) THEN
        -- Если записей нет, создаем новую запись
        INSERT INTO public.control_enter_workingdayofweek (
            id,
            created,
            modified,
            week_period,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday
        ) VALUES (
            uuid_generate_v4(),  -- Генерация нового UUID
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP,
            current_week_period,  -- Используем переименованную переменную
            TRUE,  -- Пример статуса для понедельника
            TRUE,  -- Пример статуса для вторника
            TRUE,  -- Пример статуса для среды
            TRUE,  -- Пример статуса для четверга
            FALSE,  -- Пример статуса для пятницы
            FALSE,  -- Пример статуса для субботы
            FALSE   -- Пример статуса для воскресенья
        );
        RAISE NOTICE 'Создана запись для недели с % до %', start_date, end_date;
    ELSE
        RAISE NOTICE 'Запись уже существует для недели с % до %', start_date, end_date;
    END IF;
END;
$$;


COMMENT ON FUNCTION public.create_weekly_working_day_status IS 'Создает записи в таблице control_enter_workingdayofweek для недели через две недели от текущей даты, если они отсутствуют.';
SELECT cron.schedule('create_weekly_working_day_status', '10 0 * * 1', $$ SELECT public.create_weekly_working_day_status(); $$);

