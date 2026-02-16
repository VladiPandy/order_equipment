"""
SQL-запросы для модуля информации
"""

# Запросы для info_booking_lists

# Запрос для администраторов
INFO_BOOKING_LISTS_ADMIN_QUERY = """
    SELECT y.project_name, x.date_booking, z.analyze_name, e.name, 
    concat(ex.last_name,' ',ex.first_name,' ',ex.patronymic), x.status
    FROM projects_booking x
    JOIN "project" y ON y.id = x.project_id
    JOIN "analyze" z ON z.id = x.analyse_id
    JOIN equipment e ON e.id = x.equipment_id
    JOIN executor ex ON ex.id = x.executor_id
    WHERE x.date_booking BETWEEN :start_date AND :end_date
    and x.is_delete = False
"""

# Запрос для обычных пользователей
INFO_BOOKING_LISTS_USER_QUERY = """
    WITH uuid_project AS (
        SELECT id, project_name FROM "project" WHERE project_nick = :username
    )
    SELECT y.project_name, x.date_booking, z.analyze_name, e.name, 
    concat(ex.last_name,' ',ex.first_name,' ',ex.patronymic), x.status
    FROM projects_booking x
    JOIN uuid_project y ON y.id = x.project_id
    JOIN "analyze" z ON z.id = x.analyse_id
    JOIN equipment e ON e.id = x.equipment_id
    JOIN executor ex ON ex.id = x.executor_id
    
    WHERE x.date_booking BETWEEN :start_date AND :end_date
    and x.is_delete = False
"""

# Запросы для info_bookings

# Запрос для администраторов
INFO_BOOKINGS_ADMIN_QUERY = """
    SELECT x.id, y.project_name, x.date_booking, z.analyze_name, e.name
     , concat(ex.last_name,' ',ex.first_name,' ',ex.patronymic),x.count_analyses, x.status, x.comment
    FROM projects_booking x
    JOIN "project" y ON y.id = x.project_id
    JOIN "analyze" z ON z.id = x.analyse_id
    JOIN equipment e ON e.id = x.equipment_id
    JOIN executor ex ON ex.id = x.executor_id
    WHERE x.date_booking BETWEEN :start_date AND :end_date
    and x.is_delete = False
"""

# Запрос для обычных пользователей
INFO_BOOKINGS_USER_QUERY = """
    WITH uuid_project AS (
        SELECT id, project_name FROM "project" WHERE project_nick = :username
    )
    SELECT x.id, y.project_name, x.date_booking, z.analyze_name, e.name
        , concat(ex.last_name,' ',ex.first_name,' ',ex.patronymic), x.count_analyses, x.status, x.comment
    FROM projects_booking x
    JOIN uuid_project y ON y.id = x.project_id
    JOIN "analyze" z ON z.id = x.analyse_id
    JOIN equipment e ON e.id = x.equipment_id
    JOIN executor ex ON ex.id = x.executor_id

    WHERE x.date_booking BETWEEN :start_date AND :end_date
    and x.is_delete = False
"""

# Запросы для info_executor

# Запрос для администраторов
INFO_EXECUTOR_ADMIN_QUERY = """
    select concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) fio
        , max(case 
            when cew.monday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 1 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 1 and cew.monday = 'Выходной' then 'Выходной'
            else ''
        end) as monday
        ,  max(case 
            when cew.tuesday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 2 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 2 and cew.tuesday = 'Выходной' then 'Выходной'
            else ''
        end) as tuesday
        ,  max(case 
            when cew.wednesday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 3 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 3 and cew.wednesday = 'Выходной' then 'Выходной'
            else ''
        end) as wednesday
        ,  max(case 
            when cew.thursday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 4 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 4 and cew.thursday = 'Выходной' then 'Выходной'
            else ''
        end) as thursday
        ,  max(case 
            when cew.friday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 5 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 5 and cew.friday = 'Выходной' then 'Выходной'
            else ''
        end) as friday
        ,  max(case 
            when cew.saturday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 6 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 6 and cew.saturday = 'Выходной' then 'Выходной'
            else ''
        end) as saturday
        ,  max(case 
            when cew.sunday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 0 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 0 and cew.sunday = 'Выходной' then 'Выходной'
            else ''
        end) as sunday
    from executor e 
    left join projects_booking pb on pb.executor_id = e.id 
    left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
    left join analyze a on pb.analyse_id = a.id
    where pb.date_booking between :start_date and :end_date and (cew.executor_id is not null
    and to_date(split_part(cew.week_period,'-',1),'dd.mm.YYYY') = :start_date::date 
    and to_date(split_part(cew.week_period,'-',2),'dd.mm.YYYY') = :end_date::date)
    group by concat(e.last_name,e.first_name,coalesce(e.patronymic,''))
"""

# Запрос для обычных пользователей
INFO_EXECUTOR_USER_QUERY = """
    select concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) fio
        , max(case 
            when cew.monday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 1 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 1 and cew.monday = 'Выходной' then 'Выходной'
            else ''
        end) as monday
        ,  max(case 
            when cew.tuesday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 2 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 2 and cew.tuesday = 'Выходной' then 'Выходной'
            else ''
        end) as tuesday
        ,  max(case 
            when cew.wednesday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 3 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 3 and cew.wednesday = 'Выходной' then 'Выходной'
            else ''
        end) as wednesday
        ,  max(case 
            when cew.thursday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 4 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 4 and cew.thursday = 'Выходной' then 'Выходной'
            else ''
        end) as thursday
        ,  max(case 
            when cew.friday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 5 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 5 and cew.friday = 'Выходной' then 'Выходной'
            else ''
        end) as friday
        ,  max(case 
            when cew.saturday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 6 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 6 and cew.saturday = 'Выходной' then 'Выходной'
            else ''
        end) as saturday
        ,  max(case 
            when cew.sunday = 'Выходной' then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 0 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 0 and cew.sunday = 'Выходной' then 'Выходной'
            else ''
        end) as sunday
    from executor e 
    left join projects_booking pb on pb.executor_id = e.id 
    left join project p on p.id = pb.project_id and p.project_nick = :username
    left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
    left join analyze a on pb.analyse_id = a.id
    where pb.date_booking between :start_date and :end_date and (cew.executor_id is not null
    and to_date(split_part(cew.week_period,'-',1),'dd.mm.YYYY') = :start_date::date 
    and to_date(split_part(cew.week_period,'-',2),'dd.mm.YYYY') = :end_date::date)
    group by concat(e.last_name,e.first_name,coalesce(e.patronymic,''))
"""

# Запросы для info_equipment

# Запрос для администраторов
INFO_EQUIPMENT_ADMIN_QUERY = """
    select e.name
        , max(case 
            when cdw.monday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 1 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 1 and cdw.monday = False then 'Выходной'
            else ''
        end) as monday
        ,  max(case 
            when cdw.tuesday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 2 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 2 and cdw.tuesday = False then 'Выходной'
            else ''
        end) as tuesday
        ,  max(case 
            when cdw.wednesday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 3 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 3 and cdw.wednesday = False then 'Выходной'
            else ''
        end) as wednesday
        ,  max(case 
            when cdw.thursday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 4 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 4 and cdw.thursday = False then 'Выходной'
            else ''
        end) as thursday
        ,  max(case 
            when cdw.friday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 5 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 5 and cdw.friday = False then 'Выходной'
            else ''
        end) as friday
        ,  max(case 
            when cdw.saturday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 6 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 6 and cdw.saturday = False then 'Выходной'
            else ''
        end) as saturday
        ,  max(case 
            when cdw.sunday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 0 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 0 and cdw.sunday = False then 'Выходной'
            else ''
        end) as sunday
    from equipment e 
    left join projects_booking pb on pb.equipment_id = e.id 
    left join control_enter_workingdayofweek cdw on 1=1
    left join analyze a on pb.analyse_id = a.id
    where pb.date_booking between :start_date and :end_date and (cdw.id is not null
      and to_date(split_part(cdw.week_period,'-',1),'dd.mm.YYYY') = :start_date::date 
    and to_date(split_part(cdw.week_period,'-',2),'dd.mm.YYYY') = :end_date::date)
    group by e.name
"""

# Запрос для обычных пользователей
INFO_EQUIPMENT_USER_QUERY = """
    select e.name
        , max(case 
            when cdw.monday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 1 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 1 and cdw.monday = False then 'Выходной'
            else ''
        end) as monday
        ,  max(case 
            when cdw.tuesday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 2 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 2 and cdw.tuesday = False then 'Выходной'
            else ''
        end) as tuesday
        ,  max(case 
            when cdw.wednesday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 3 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 3 and cdw.wednesday = False then 'Выходной'
            else ''
        end) as wednesday
        ,  max(case 
            when cdw.thursday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 4 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 4 and cdw.thursday = False then 'Выходной'
            else ''
        end) as thursday
        ,  max(case 
            when cdw.friday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 5 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 5 and cdw.friday = False then 'Выходной'
            else ''
        end) as friday
        ,  max(case 
            when cdw.saturday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 6 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 6 and cdw.saturday = False then 'Выходной'
            else ''
        end) as saturday
        ,  max(case 
            when cdw.sunday = False then 'Выходной'
            when date_part('dow', pb.date_booking::date) = 0 and a.analyze_name is not null then a.analyze_name
            when date_part('dow', pb.date_booking::date) = 0 and cdw.sunday = False then 'Выходной'
            else ''
        end) as sunday
    from equipment e 
    left join projects_booking pb on pb.equipment_id = e.id 
    left join project p on p.id = pb.project_id and p.project_nick = :username
    left join control_enter_workingdayofweek cdw on 1=1
    left join analyze a on pb.analyse_id = a.id
    where pb.date_booking between :start_date and :end_date and (cdw.id is not null
      and to_date(split_part(cdw.week_period,'-',1),'dd.mm.YYYY') = :start_date::date 
    and to_date(split_part(cdw.week_period,'-',2),'dd.mm.YYYY') = :end_date::date)
    group by e.name
"""

# Запрос для получения информации о проекте
PROJECT_INFO_QUERY = """
    SELECT responsible_person,project_name, is_priority , False as is_admin  FROM \"project\" WHERE project_nick = '{username}' 
    UNION ALL
    SELECT admin_person responsible_person ,admin_nick project_name, True as is_priority, True as is_admin FROM \"adminstrator\" WHERE admin_nick = '{username}' LIMIT 1;
"""

# Запрос для проверки открытого глобального окна
OPEN_GLOBAL_WINDOW_QUERY = """
    SELECT id  FROM \"control_enter_openwindowforordering\" 
    WHERE start_date = '{date_str}'
    and CAST('{time_str}' AS time) between CAST(start_time AS time) and CAST(end_time AS time) and (for_priority = {is_priority} or for_priority = 
                        CASE 
                            WHEN {is_priority} = True THEN False
                            ELSE False
                        END)
    ;
"""

# Запрос для проверки открытой локальной регистрации
OPEN_LOCAL_REGISTRATION_QUERY = """
    SELECT id  FROM \"control_enter_isopenregistration\" 
    WHERE is_open = True
    ;
"""

BOOKING_INFO_STAFF = """
    SELECT x.id, y.project_name, x.date_booking, z.analyze_name, e.name
     , concat(ex.last_name,' ',ex.first_name,' ',ex.patronymic),x.count_analyses, x.status, x.comment,
     COALESCE(m.messages_count, 0) AS messages_count,
     CASE
        WHEN m.messages_count = 0 THEN NULL
        ELSE (m.last_author_username = '{username}')
    END AS last_message_is_me
    FROM projects_booking x
    JOIN "project" y ON y.id = x.project_id
    JOIN "analyze" z ON z.id = x.analyse_id
    JOIN equipment e ON e.id = x.equipment_id
    JOIN executor ex ON ex.id = x.executor_id
    LEFT JOIN (
        SELECT
            booking_id,
            COUNT(*) AS messages_count,
            (
                SELECT author_username
                FROM public.projects_booking_messages m2
                WHERE m2.booking_id = m.booking_id
                  AND m2.is_deleted = FALSE
                ORDER BY m2.created_at DESC
                LIMIT 1
            ) AS last_author_username
        FROM public.projects_booking_messages m
        WHERE m.is_deleted = FALSE
        GROUP BY booking_id
    ) m ON m.booking_id = x.id
    WHERE x.date_booking BETWEEN '{start_date}' AND '{end_date}'
    and x.is_delete = False
    order by  x.date_booking desc,y.project_name, z.analyze_name, e.name, concat(ex.last_name,' ',ex.first_name,' ',ex.patronymic)
"""

BOOKING_INFO_USER = """
    WITH uuid_project AS (
        SELECT id, project_name FROM "project" WHERE project_nick = '{username}'
    )
    SELECT x.id, y.project_name, x.date_booking, z.analyze_name, e.name
        , concat(ex.last_name,' ',ex.first_name,' ',ex.patronymic), x.count_analyses, x.status, x.comment,
        -- количество сообщений
        COALESCE(m.messages_count, 0) AS messages_count,
        -- последнее сообщение мое / не мое
        CASE
            WHEN m.messages_count = 0 THEN NULL
            ELSE (m.last_author_username = '{username}')
        END AS last_message_is_me
    FROM projects_booking x
    JOIN uuid_project y ON y.id = x.project_id
    JOIN "analyze" z ON z.id = x.analyse_id
    JOIN equipment e ON e.id = x.equipment_id
    JOIN executor ex ON ex.id = x.executor_id
    LEFT JOIN (
        SELECT
            booking_id,
            COUNT(*) AS messages_count,
            (
                SELECT author_username
                FROM public.projects_booking_messages m2
                WHERE m2.booking_id = m.booking_id
                  AND m2.is_deleted = FALSE
                ORDER BY m2.created_at DESC
                LIMIT 1
            ) AS last_author_username
        FROM public.projects_booking_messages m
        WHERE m.is_deleted = FALSE
        GROUP BY booking_id
    ) m ON m.booking_id = x.id

    WHERE x.date_booking BETWEEN '{start_date}' AND '{end_date}'
    and x.is_delete = False
    order by x.date_booking desc ,y.project_name, z.analyze_name, e.name, concat(ex.last_name,' ',ex.first_name,' ',ex.patronymic)
"""

RATINGS_QUERY = """
SELECT
    concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) AS executor,
    ROUND(AVG(
        CASE
            WHEN ft.booking_id IS NOT NULL THEN
                (
                    CASE WHEN ft.question_1 IS TRUE THEN 1 ELSE 0 END +
                    CASE WHEN ft.question_2 IS TRUE THEN 1 ELSE 0 END +
                    CASE WHEN ft.question_3 IS TRUE THEN 1 ELSE 0 END
                ) / 3.0
            ELSE NULL
        END
    ),2) AS avg_total,
    ROUND(AVG(
        CASE
            WHEN ft.booking_id IS NOT NULL
                THEN CASE WHEN ft.question_1 IS TRUE THEN 1 ELSE 0 END
            ELSE NULL
        END
    ),2) AS avg_on_time,
    ROUND(AVG(
        CASE
            WHEN ft.booking_id IS NOT NULL
                THEN CASE WHEN ft.question_2 IS TRUE THEN 1 ELSE 0 END
            ELSE NULL
        END
    ),2) AS avg_full_set,
    ROUND(AVG(
        CASE
            WHEN ft.booking_id IS NOT NULL
                THEN CASE WHEN ft.question_3 IS TRUE THEN 1 ELSE 0 END
            ELSE NULL
        END
    ),2) AS avg_quality,
    SUM(
        CASE
            WHEN ft.booking_id IS NOT NULL THEN 1
            ELSE 0
        END
    ) AS total_answer_analyses,
    SUM(
        CASE
            WHEN coalesce(pb.status,'') in ('Выполнено','Оценить') THEN 1
            ELSE 0
        END
    ) AS total_analyses
FROM executor e
JOIN projects_booking pb ON pb.executor_id = e.id
LEFT JOIN feedback_task ft ON ft.booking_id = pb.id
WHERE pb.is_delete = false and date_booking BETWEEN :date_start AND :date_end
GROUP BY executor
order by concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,''))
"""