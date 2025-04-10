"""
SQL-запросы для модуля бронирования
"""

# Запрос для получения возможных вариантов бронирования
POSSIBLE_CREATE_BOOKING_QUERY = """
    WITH uuid_project AS (
        SELECT id, project_name, is_priority, responsible_person FROM "project" WHERE project_nick = :username
    ),
    executor_filter AS (
        SELECT e.id, concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) as fio
        FROM executor e
        WHERE (
            :executor_id is null 
            or :executor_id = e.id
        )
    ),
    analyse_filter AS (
        SELECT a.id, a.analyze_name
        FROM analyze a
        WHERE (
            :analyse_id is null 
            or :analyse_id = a.id
        )
    ),
    equipment_filter AS (
        SELECT e.id, e.name
        FROM equipment e
        WHERE (
            :equipment_id is null 
            or :equipment_id = e.id
        )
    )
    SELECT  ef.id as executor_id, 
            af.id as analyse_id,
            eqf.id as equipment_id,
            ef.fio as executor_fio,
            af.analyze_name,
            eqf.name as equipment_name,
            p.project_name,
            p.responsible_person 
    FROM uuid_project p, 
         executor_filter ef,
         analyse_filter af,
         equipment_filter eqf
    order by ef.fio, af.analyze_name;
"""

# Запрос для проверки свободного окна
CHECK_FREE_WINDOW_QUERY = """
    SELECT id, day_of_week, to_char(start_time, 'HH24:MI') as start_time, to_char(end_time, 'HH24:MI') as end_time
    FROM times_booking
    WHERE not EXISTS (
        SELECT 1 
        FROM projects_booking pb
        WHERE pb.time_id = times_booking.id
          AND pb.date_booking = :date_booking
          AND pb.is_delete = false
    )
      AND day_of_week = :dow;
"""

# Запрос для вставки записи бронирования
INSERT_BOOKING_QUERY = """
    INSERT INTO projects_booking (
        project_id, time_id, date_booking, count_analyses, analyse_id, equipment_id, executor_id, status, comment
    )
    VALUES (
        :project_id, :time_id, :date_booking, :count_analyses, :analyse_id, :equipment_id, :executor_id, 'Заявка создана', ''
    )
    RETURNING id;
"""

# Запрос для получения возможных изменений бронирования
GET_BOOKING_DETAILS_QUERY = """
    SELECT pb.id, pb.project_id, p.project_name, pb.time_id, pb.date_booking, pb.count_analyses, 
           pb.analyse_id, a.analyze_name, pb.equipment_id, e.name, pb.executor_id, 
           concat(ex.last_name,' ',ex.first_name,' ',coalesce(ex.patronymic,'')) as fio,
           t.day_of_week, to_char(t.start_time, 'HH24:MI') as start_time, to_char(t.end_time, 'HH24:MI') as end_time
    FROM projects_booking pb
    JOIN "project" p ON p.id = pb.project_id
    JOIN "analyze" a ON a.id = pb.analyse_id
    JOIN equipment e ON e.id = pb.equipment_id
    JOIN executor ex ON ex.id = pb.executor_id
    JOIN times_booking t ON t.id = pb.time_id
    WHERE pb.id = :booking_id
      AND pb.is_delete = false;
"""

# Запрос для обновления записи бронирования
UPDATE_BOOKING_QUERY = """
    UPDATE projects_booking
    SET time_id = :time_id,
        date_booking = :date_booking,
        count_analyses = :count_analyses,
        analyse_id = :analyse_id,
        equipment_id = :equipment_id,
        executor_id = :executor_id,
        status = 'Заявка изменена'
    WHERE id = :booking_id
    RETURNING id;
"""

# Запрос для отмены бронирования
CANCEL_BOOKING_QUERY = """
    UPDATE projects_booking
    SET is_delete = true,
        status = 'Заявка отменена'
    WHERE id = :booking_id
    RETURNING id;
"""

# Запрос для добавления обратной связи
UPDATE_BOOKING_FEEDBACK_QUERY = """
    UPDATE projects_booking
    SET comment = :comment
    WHERE id = :booking_id
    RETURNING id;
"""

# Запрос для проверки прав на бронирование
CHECK_BOOKING_PERMISSIONS_QUERY = """
    SELECT pb.id
    FROM projects_booking pb
    JOIN "project" p ON p.id = pb.project_id
    WHERE pb.id = :booking_id
      AND (p.project_nick = :username OR :is_admin = true)
      AND pb.is_delete = false;
"""

# Запросы для метода get_uuids

# Запрос для получения ID анализа по имени
GET_ANALYZE_ID_BY_NAME_QUERY = """
    SELECT id FROM "analyze" WHERE analyze_name = '{analyze_name}';
"""

# Запрос для получения имени анализа по ID
GET_ANALYZE_NAME_BY_ID_QUERY = """
    SELECT analyze_name FROM "analyze" WHERE id = {analyze_id};
"""

# Запрос для получения ID оборудования по имени
GET_EQUIPMENT_ID_BY_NAME_QUERY = """
    SELECT id FROM "equipment" WHERE name = '{equipment_name}';
"""

# Запрос для получения ID исполнителя по ФИО
GET_EXECUTOR_ID_BY_NAME_QUERY = """
    SELECT id FROM "executor" WHERE concat(first_name,' ',last_name,' ',patronymic) = '{executor_name}';
"""

# Запросы для работы с токенами

# Запрос для проверки токена
VALIDATE_TOKEN_QUERY = """
    SELECT * FROM cookie_createkey 
    WHERE cookie_key = '{cookie_key}'
    AND blocking = false
    AND expiration_date > now();
"""

# Запрос для создания нового токена
CREATE_TOKEN_QUERY = """
    INSERT INTO public.block_booking
    (project_id)
    VALUES ('{project_id}')
    RETURNING cookies_key
"""


# Запрос для блокировки токена
BLOCK_TOKEN_QUERY = """
    UPDATE cookie_createkey
    SET blocking = true
    WHERE cookie_key = '{cookie_key}';
"""

# Запросы для блокировки периода

# Запрос для создания блокировки периода
CREATE_BLOCKING_PERIOD_QUERY = """
    INSERT INTO blocking_period (cookie_key, date_booking, analyse_id, equipment_id, executor_id, expiration_date) 
    VALUES ('{cookie_key}', '{date_booking}', {analyse_id}, {equipment_id}, {executor_id}, now() + interval '10 minutes')
    RETURNING id;
"""

# Запрос для обновления блокировки периода
UPDATE_BLOCKING_PERIOD_QUERY = """
    UPDATE public.block_booking
    SET 
        date_booking = '{date_booking}' ,
        analyse_id = {analyse_id} ,
        equipment_id = {equipment_id},
        executor_id =  {executor_id} ,
        update_timestamp = now()
    WHERE cookies_key = '{cookie_key}' 
"""

# Запрос для проверки существования блокировки
CHECK_BLOCKING_PERIOD_QUERY = """
    SELECT *
    FROM blocking_period bp
    WHERE bp.date_booking = '{date_booking}'
    AND bp.analyse_id = {analyse_id}
    AND bp.equipment_id = {equipment_id}
    AND bp.executor_id = {executor_id}
    AND bp.cookie_key != '{cookie_key}'
    AND bp.expiration_date > now()
    LIMIT 1;
"""

# Запрос для удаления истекших блокировок
DELETE_EXPIRED_BLOCKINGS_QUERY = """
    DELETE FROM blocking_period
    WHERE expiration_date < now();
""" 