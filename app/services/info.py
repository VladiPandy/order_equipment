import datetime
from datetime import timedelta
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
import pandas as pd
from typing import Dict, List, Any
import logging

from models.schemas.info import InfoProjectResponse, InfoListsRequest, \
    InfoListsResponse, InfoBookingItem, InfoEquipmentTable, InfoExecutorTable
from services.booking import UserBookingService
from sql.info_queries import BOOKING_INFO_STAFF, BOOKING_INFO_USER, RATINGS_QUERY

logger = logging.getLogger(__name__)


class UserInfoService:

    @staticmethod
    async def info_booking_lists(
            request_data: InfoListsRequest,
            user,
            db: AsyncSession,
    ) -> InfoListsResponse:
        # 1. Парсинг даты
        request_dict = request_data.dict(exclude_unset=True)

        date_booking_dict = await UserBookingService.validate_date_booking(
            request_dict)
        logger.debug("Проверенные даты бронирования: %s", date_booking_dict)

        #Формируем запрос в зависимости от роли пользователя

        if user.is_staff:
            query = text("""
                SELECT y.project_name, x.date_booking, z.analyze_name, e.name, concat(ex.last_name,' ',ex.first_name,' ',ex.patronymic), x.status
                FROM projects_booking x
                JOIN "project" y ON y.id = x.project_id
                JOIN "analyze" z ON z.id = x.analyse_id
                JOIN equipment e ON e.id = x.equipment_id
                JOIN executor ex ON ex.id = x.executor_id
                WHERE x.date_booking BETWEEN :start_date AND :end_date
                and x.is_delete = False
            """)
            params = {"start_date": date_booking_dict['date_start'],
                      "end_date": date_booking_dict['date_end']}
        else:
            query = text("""
                WITH uuid_project AS (
                    SELECT id, project_name FROM "project" WHERE project_nick = :username
                )
                SELECT y.project_name, x.date_booking, z.analyze_name, e.name, concat(ex.last_name,' ',ex.first_name,' ',ex.patronymic), x.status
                FROM projects_booking x
                JOIN uuid_project y ON y.id = x.project_id
                JOIN "analyze" z ON z.id = x.analyse_id
                JOIN equipment e ON e.id = x.equipment_id
                JOIN executor ex ON ex.id = x.executor_id
                
                WHERE x.date_booking BETWEEN :start_date AND :end_date
                and x.is_delete = False
            """)
            params = {"username": user.username,
                      "start_date": date_booking_dict['date_start'],
                      "end_date": date_booking_dict['date_end']}

        result = await db.execute(query, params)
        rows = result.fetchall()

        # Если нет записей, возвращаем пустые списки
        if not rows:
            logger.info("Нет записей для указанных дат.")
            return InfoListsResponse(
                project=[],
                date=[],
                analyse=[],
                equipment=[],
                executor=[],
                status=[]
            )

        # 3. Агрегируем данные в наборы (для уникальности)
        projects_set = set()
        date_bookings_set = set()
        analyzes_set = set()
        equipments_set = set()
        executors_set = set()
        statuses_set = set()

        for row in rows:
            # row = (project_name, date_booking, analyze_name, equipment name, executor_fio, status)
            projects_set.add(row[0])
            # Приводим дату в формат "dd.mm.yyyy"
            if row[1]:
                date_bookings_set.add(row[1].strftime("%d.%m.%Y"))
            analyzes_set.add(row[2])
            equipments_set.add(row[3])
            executors_set.add(row[4])
            statuses_set.add(row[5])
        logger.debug("Уникальные проекты: %s", projects_set)
        
        # Для не-админов список проектов оставляем пустым
        projects = list(projects_set) # if user.is_staff else []

        return InfoListsResponse(
            project=projects,
            date=list(date_bookings_set),
            analyse=list(analyzes_set),
            equipment=list(equipments_set),
            executor=list(executors_set),
            status=list(statuses_set)
        )

    @staticmethod
    async def info_bookings(
            request_data: InfoListsRequest,
            user,
            db: AsyncSession,
    ) -> InfoBookingItem:
        # 1. Парсинг даты
        request_dict = request_data.dict(exclude_unset=True)
        logger.debug("Запрос данных бронирования: %s", request_dict)
        
        date_booking_dict = await UserBookingService.validate_date_booking(
            request_dict)


        # Формируем запрос в зависимости от роли пользователя

        if user.is_staff:
            query = (
                text(
                    BOOKING_INFO_STAFF.format(
                        start_date = date_booking_dict['date_start'],
                        end_date = date_booking_dict['date_end'],
                        username=user.username,
                    )
                )
            )
            # query = text("""
            #         SELECT x.id, y.project_name, x.date_booking, z.analyze_name, e.name
            #          , concat(ex.first_name,' ',ex.last_name,' ',ex.patronymic),x.count_analyses, x.status, x.comment
            #         FROM projects_booking x
            #         JOIN "project" y ON y.id = x.project_id
            #         JOIN "analyze" z ON z.id = x.analyse_id
            #         JOIN equipment e ON e.id = x.equipment_id
            #         JOIN executor ex ON ex.id = x.executor_id
            #         WHERE x.date_booking BETWEEN :start_date AND :end_date
            #         and x.is_delete = False
            #     """)
            # params = {"start_date": date_booking_dict['date_start'],
            #           "end_date": date_booking_dict['date_end']}
        else:
            query = (
                text(
                    BOOKING_INFO_USER.format(
                        start_date=date_booking_dict['date_start'],
                        end_date=date_booking_dict['date_end'],
                        username=user.username
                    )
                )
            )

            # query = text("""
            #         WITH uuid_project AS (
            #             SELECT id, project_name FROM "project" WHERE project_nick = :username
            #         )
            #         SELECT x.id, y.project_name, x.date_booking, z.analyze_name, e.name
            #             , concat(ex.first_name,' ',ex.last_name,' ',ex.patronymic), x.count_analyses, x.status, x.comment
            #         FROM projects_booking x
            #         JOIN uuid_project y ON y.id = x.project_id
            #         JOIN "analyze" z ON z.id = x.analyse_id
            #         JOIN equipment e ON e.id = x.equipment_id
            #         JOIN executor ex ON ex.id = x.executor_id
            #
            #         WHERE x.date_booking BETWEEN :start_date AND :end_date
            #         and x.is_delete = False
            #     """)
            # params = {"username": user.username,
            #           "start_date": date_booking_dict['date_start'],
            #           "end_date": date_booking_dict['date_end']}

        result = await db.execute(query)
        rows = result.fetchall()

        logger.debug("Полученные данные бронирования: %s", rows)
        if not rows:
            logger.info("Нет данных для указанных дат.")
            return []  # Возвращаем пустой список, если данных нет

        bookings: List[InfoBookingItem] = []
        for row in rows:
            # row: (id, project, date_booking, analyze, equipment, executor, count_samples, status, comment)
            logger.debug("Обработка строки бронирования: %s", row)
            
            try:
                date_booking_str = row[2].strftime("%d.%m.%Y") if row[2] else ""
            except Exception:
                logger.error("Ошибка при форматировании даты: %s", e)
                
                date_booking_str = str(row[2])
            booking_item = InfoBookingItem(
                id=row[0],
                project=row[1],
                date=date_booking_str,
                analyse=row[3],
                equipment=row[4],
                executor=row[5],
                samples=row[6],
                status=row[7],
                comment=row[8] if row[8] is not None else "",
                messages_count=row[9],
                last_message_is_me= row[10],
            )
            bookings.append(booking_item)

        logger.debug("Сформированные бронирования: %s", bookings)
        return bookings


    @staticmethod
    async def download_bookings_excel(
            request_data: InfoListsRequest,
            user,
            db: AsyncSession,
    ) -> Response:
        request_dict = request_data.dict(exclude_unset=True)
        date_booking_dict = await UserBookingService.validate_date_booking(request_dict)

        if user.is_staff:
            query = (
                text(
                    BOOKING_INFO_STAFF.format(
                        start_date=date_booking_dict['date_start'],
                        end_date=date_booking_dict['date_end'],
                        username=user.username
                    )
                )
            )
        else:
            query = (
                text(
                    BOOKING_INFO_USER.format(
                        start_date=date_booking_dict['date_start'],
                        end_date=date_booking_dict['date_end'],
                        username=user.username
                    )
                )
            )
        result = await db.execute(query)
        rows = result.fetchall()

        df = pd.DataFrame(rows, columns=[
            "id", "Проект", "Дата", "Анализ", "Оборудование", "Исполнитель", "Кол-во проб", "Статус", "Комментарий", "Сообщений", "Последнее мое сообщение"
        ])
        if not df.empty:
            df["Дата"] = df["Дата"].apply(lambda x: x.strftime("%d.%m.%Y") if hasattr(x, "strftime") else x)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Бронирования")
        output.seek(0)

        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers={"Content-Disposition": f"attachment; filename={date_booking_dict['date_start']}_{date_booking_dict['date_end']}_booking.xlsx"})


    @staticmethod
    async def info_executor(
            request_data: InfoListsRequest,
            user,
            db: AsyncSession,
    ) -> InfoBookingItem:
        request_dict = request_data.dict(exclude_unset=True)
        logger.debug("Запрос данных исполнителей: %s", request_dict)
        
        date_booking_dict = await UserBookingService.validate_date_booking(
            request_dict)
        # Формируем запрос в зависимости от роли пользователя

        if user.is_staff:
            query = text(f"""
                        with monday as (
                        SELECT
                            e.id
                            , concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as monday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 1
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),tuesday as (
                        SELECT
                            e.id
                            ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as tuesday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 2
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),wednesday as (
                        SELECT
                        e.id
                        ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as wednesday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 3
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),thursday as (
                        SELECT
                        e.id
                        ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as thursday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 4
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),friday as (
                        SELECT
                        e.id
                        ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as friday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 5
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),saturday as (
                        SELECT
                        e.id
                        ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as saturday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 6
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),sunday as (
                        SELECT
                        e.id
                            ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as sunday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 0
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    )
                    select coalesce(monday.fio,tuesday.fio,wednesday.fio,thursday.fio,friday.fio,saturday.fio,sunday.fio) fio
                        , case 
                            when cew.monday = 'Выходной' then 'Выходной'
                            else coalesce(monday.monday,'')
                         end monday
                         , case 
                            when cew.tuesday = 'Выходной' then 'Выходной'
                            else coalesce(tuesday.tuesday,'')
                         end tuesday
                         , case 
                            when cew.wednesday = 'Выходной' then 'Выходной'
                            else coalesce(wednesday.wednesday,'')
                         end wednesday
                         , case 
                            when cew.thursday = 'Выходной' then 'Выходной'
                            else coalesce(thursday.thursday,'')
                         end thursday
                         , case 
                            when cew.friday = 'Выходной' then 'Выходной'
                            else coalesce(friday.friday,'')
                         end friday
                         , case 
                            when cew.saturday = 'Выходной' then 'Выходной'
                            else coalesce(saturday.saturday,'')
                         end saturday
                         , case 
                            when cew.sunday = 'Выходной' then 'Выходной'
                            else coalesce(sunday.sunday,'')
                         end sunday
                    from monday
                    full join tuesday USING(fio,rn)
                    full join wednesday USING(fio,rn)
                    full join thursday USING(fio,rn)
                    full join friday USING(fio,rn)
                    full join saturday USING(fio,rn)
                    full join sunday USING(fio,rn)
                    left join control_enter_workerweekstatus cew on coalesce(monday.id,tuesday.id,wednesday.id,thursday.id,friday.id,saturday.id,sunday.id) = cew.executor_id
                        and  cew.week_period = '{request_dict['start']}-{request_dict['end']}'
                    order by coalesce(monday.fio,tuesday.fio,wednesday.fio,thursday.fio,friday.fio,saturday.fio,sunday.fio)
                    , monday.rn,tuesday.rn,wednesday.rn,thursday.rn,friday.rn,saturday.rn,sunday.rn
                    """)
            params = {"start_date": date_booking_dict['date_start'],
                      "end_date": date_booking_dict['date_end']}
        else:
            query = text("""
                        WITH uuid_project AS (
                            SELECT id, project_name FROM "project" WHERE project_nick = :username
                        )
                        select concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
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
                        left join "analyze" a  on a.id = pb.analyse_id  
                        JOIN uuid_project y ON y.id = pb.project_id
                        where pb.is_delete = false
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')), coalesce(a.analyze_name,'')
                    """)
            params = {"username": user.username,
                      "start_date": date_booking_dict['date_start'],
                      "end_date": date_booking_dict['date_end']}

        result = await db.execute(query, params)
        rows = result.fetchall()

        logger.debug("Полученные данные исполнителей: %s", rows)
        if not rows:
            logger.info("Нет данных для указанных дат.")
            return []  # Возвращаем пустой список, если данных нет

        bookings = []
        for row in rows:
            # row: (id, project, date_booking, analyze, equipment, executor, count_samples, status, comment)
            logger.debug("Обработка строки исполнителя: %s", row)

            booking_item = InfoExecutorTable(
                executor=row[0],
                monday=row[1],
                tuesday=row[2],
                wednesday=row[3],
                thursday=row[4],
                friday=row[5],
                saturday=row[6],
                sunday=row[7]
            )
            bookings.append(booking_item)
        logger.debug("Сформированные исполнители: %s", bookings)
        return bookings


    @staticmethod
    async def download_executor_excel(
            request_data: InfoListsRequest,
            user,
            db: AsyncSession,
    ) -> Response:

        request_dict = request_data.dict(exclude_unset=True)
        date_booking_dict = await UserBookingService.validate_date_booking(request_dict)

        if user.is_staff:
            query = text(f"""
                with monday as (
                        SELECT
                            e.id
                            , concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as monday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 1
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),tuesday as (
                        SELECT
                            e.id
                            ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as tuesday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 2
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),wednesday as (
                        SELECT
                        e.id
                        ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as wednesday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 3
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),thursday as (
                        SELECT
                        e.id
                        ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as thursday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 4
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),friday as (
                        SELECT
                        e.id
                        ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as friday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 5
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),saturday as (
                        SELECT
                        e.id
                        ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as saturday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 6
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    ),sunday as (
                        SELECT
                        e.id
                            ,concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
                            , max(a.analyze_name) as sunday
                            , row_number() over(partition by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')) order by a.analyze_name) rn
                        from executor e 
                        left join projects_booking pb on pb.executor_id = e.id 
                        ----left join control_enter_workerweekstatus cew on e.id = cew.executor_id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 0
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,e.first_name,coalesce(e.patronymic,'')), a.analyze_name, e.id
                    )
                    select coalesce(monday.fio,tuesday.fio,wednesday.fio,thursday.fio,friday.fio,saturday.fio,sunday.fio) fio
                        , case 
                            when cew.monday = 'Выходной' then 'Выходной'
                            else coalesce(monday.monday,'')
                         end monday
                         , case 
                            when cew.tuesday = 'Выходной' then 'Выходной'
                            else coalesce(tuesday.tuesday,'')
                         end tuesday
                         , case 
                            when cew.wednesday = 'Выходной' then 'Выходной'
                            else coalesce(wednesday.wednesday,'')
                         end wednesday
                         , case 
                            when cew.thursday = 'Выходной' then 'Выходной'
                            else coalesce(thursday.thursday,'')
                         end thursday
                         , case 
                            when cew.friday = 'Выходной' then 'Выходной'
                            else coalesce(friday.friday,'')
                         end friday
                         , case 
                            when cew.saturday = 'Выходной' then 'Выходной'
                            else coalesce(saturday.saturday,'')
                         end saturday
                         , case 
                            when cew.sunday = 'Выходной' then 'Выходной'
                            else coalesce(sunday.sunday,'')
                         end sunday
                    from monday
                    full join tuesday USING(fio,rn)
                    full join wednesday USING(fio,rn)
                    full join thursday USING(fio,rn)
                    full join friday USING(fio,rn)
                    full join saturday USING(fio,rn)
                    full join sunday USING(fio,rn)
                    left join control_enter_workerweekstatus cew on coalesce(monday.id,tuesday.id,wednesday.id,thursday.id,friday.id,saturday.id,sunday.id) = cew.executor_id
                        and  cew.week_period = '{request_dict['start']}-{request_dict['end']}'
                    order by coalesce(monday.fio,tuesday.fio,wednesday.fio,thursday.fio,friday.fio,saturday.fio,sunday.fio)
                    , monday.rn,tuesday.rn,wednesday.rn,thursday.rn,friday.rn,saturday.rn,sunday.rn
            """)
            params = {"start_date": date_booking_dict['date_start'], "end_date": date_booking_dict['date_end']}
        else:
            query = text("""
                WITH uuid_project AS (
                            SELECT id, project_name FROM "project" WHERE project_nick = :username
                        )
                        select concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')) fio
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
                        left join "analyze" a  on a.id = pb.analyse_id  
                        JOIN uuid_project y ON y.id = pb.project_id
                        where pb.is_delete = false
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.last_name,' ',e.first_name,' ',coalesce(e.patronymic,'')), coalesce(a.analyze_name,'')
            """)
            params = {"username": user.username, "start_date": date_booking_dict['date_start'], "end_date": date_booking_dict['date_end']}

        result = await db.execute(query, params)
        rows = result.fetchall()

        df = pd.DataFrame(rows, columns=["Исполнитель", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"])
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Исполнители")
        output.seek(0)

        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers={"Content-Disposition": f"attachment; filename={date_booking_dict['date_start']}_{date_booking_dict['date_end']}_executors.xlsx"})



    @staticmethod
    async def info_equipment(
            request_data: InfoListsRequest,
            user,
            db: AsyncSession,
    ) -> InfoBookingItem:
        # 1. Парсинг даты
        request_dict = request_data.dict(exclude_unset=True)
        logger.debug("Запрос данных оборудования: %s", request_dict)
        date_booking_dict = await UserBookingService.validate_date_booking(
            request_dict)

        # Формируем запрос в зависимости от роли пользователя

        if user.is_staff:
            query = text("""
                        with monday as (
                            select e.name
                                , max(a.analyze_name) as monday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 1
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),tuesday as (
                            select e.name
                                , max(a.analyze_name) as tuesday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 2
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),wednesday as (
                            select e.name
                                , max(a.analyze_name) as wednesday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 3
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),thursday as (
                            select e.name
                                , max(a.analyze_name) as thursday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 4
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),friday as (
                            select e.name
                                , max(a.analyze_name) as friday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 5
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),saturday as (
                            select e.name
                                , max(a.analyze_name) as saturday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 6
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),sunday as (
                            select e.name
                                , max(a.analyze_name) as sunday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 0
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        )
                        select coalesce(monday.name,tuesday.name,wednesday.name,thursday.name,friday.name,saturday.name,sunday.name) name
                            , coalesce(monday.monday,'') monday
                            ,coalesce(tuesday.tuesday,'') tuesday
                            ,coalesce(wednesday.wednesday,'') wednesday
                            ,coalesce(thursday.thursday,'') thursday
                            ,coalesce(friday.friday,'') friday
                            ,coalesce(saturday.saturday,'') saturday
                            ,coalesce(sunday.sunday,'') sunday
                        from monday
                        full join tuesday USING(name,rn)
                        full join wednesday USING(name,rn)
                        full join thursday USING(name,rn)
                        full join friday USING(name,rn)
                        full join saturday USING(name,rn)
                        full join sunday USING(name,rn)
                    """)
            params = {"start_date": date_booking_dict['date_start'],
                      "end_date": date_booking_dict['date_end']}
        else:
            query = text("""
                        WITH uuid_project AS (
                            SELECT id, project_name FROM "project" WHERE project_nick = :username
                        )
                        select e.name
                            , max(case 
                                when date_part('dow', pb.date_booking::date) = 1 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as monday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 2 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as tuesday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 3 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as wednesday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 4 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as thursday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 5 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as friday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 6 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as saturday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 0 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as sunday
                        from equipment e 
                        left join projects_booking pb on pb.equipment_id = e.id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        JOIN uuid_project y ON y.id = pb.project_id
                        where pb.is_delete = false
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by e.name, coalesce(a.analyze_name,'')
                    """)
            params = {"username": user.username,
                      "start_date": date_booking_dict['date_start'],
                      "end_date": date_booking_dict['date_end']}

        result = await db.execute(query, params)
        rows = result.fetchall()

        logger.debug("Полученные данные оборудования: %s", rows)
        if not rows:
            logger.info("Нет данных для указанных дат.")
            return []  # Возвращаем пустой список, если данных нет

        bookings = []
        for row in rows:
            booking_item = InfoEquipmentTable(
                equipment=row[0],
                monday=row[1],
                tuesday=row[2],
                wednesday=row[3],
                thursday=row[4],
                friday=row[5],
                saturday=row[6],
                sunday=row[7]
            )
            bookings.append(booking_item)
        logger.debug("Сформированные данные оборудования: %s", bookings)
        return bookings


    @staticmethod
    async def download_equipment_excel(
            request_data: InfoListsRequest,
            user,
            db: AsyncSession,
    ) -> Response:

        request_dict = request_data.dict(exclude_unset=True)
        date_booking_dict = await UserBookingService.validate_date_booking(request_dict)

        if user.is_staff:
            query = text("""
                with monday as (
                            select e.name
                                , max(a.analyze_name) as monday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 1
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),tuesday as (
                            select e.name
                                , max(a.analyze_name) as tuesday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 2
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),wednesday as (
                            select e.name
                                , max(a.analyze_name) as wednesday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 3
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),thursday as (
                            select e.name
                                , max(a.analyze_name) as thursday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 4
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),friday as (
                            select e.name
                                , max(a.analyze_name) as friday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 5
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),saturday as (
                            select e.name
                                , max(a.analyze_name) as saturday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 6
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        ),sunday as (
                            select e.name
                                , max(a.analyze_name) as sunday
                                , row_number() over(partition by e.name order by a.analyze_name) rn
                            from equipment e 
                            left join projects_booking pb on pb.equipment_id = e.id 
                            left join "analyze" a  on a.id = pb.analyse_id  
                            where pb.is_delete = false and a.analyze_name is not null and date_part('dow', pb.date_booking::date) = 0
                            and pb.date_booking BETWEEN :start_date AND :end_date
                            group by e.name, a.analyze_name
                            order by e.name
                        )
                        select coalesce(monday.name,tuesday.name,wednesday.name,thursday.name,friday.name,saturday.name,sunday.name) name
                            , coalesce(monday.monday,'') monday
                            ,coalesce(tuesday.tuesday,'') tuesday
                            ,coalesce(wednesday.wednesday,'') wednesday
                            ,coalesce(thursday.thursday,'') thursday
                            ,coalesce(friday.friday,'') friday
                            ,coalesce(saturday.saturday,'') saturday
                            ,coalesce(sunday.sunday,'') sunday
                        from monday
                        full join tuesday USING(name,rn)
                        full join wednesday USING(name,rn)
                        full join thursday USING(name,rn)
                        full join friday USING(name,rn)
                        full join saturday USING(name,rn)
                        full join sunday USING(name,rn)
            """)
            params = {"start_date": date_booking_dict['date_start'], "end_date": date_booking_dict['date_end']}
        else:
            query = text("""
                WITH uuid_project AS (
                            SELECT id, project_name FROM "project" WHERE project_nick = :username
                        )
                        select e.name
                            , max(case 
                                when date_part('dow', pb.date_booking::date) = 1 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as monday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 2 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as tuesday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 3 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as wednesday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 4 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as thursday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 5 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as friday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 6 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as saturday
                            ,  max(case 
                                when date_part('dow', pb.date_booking::date) = 0 and a.analyze_name is not null then a.analyze_name
                                else ''
                            end) as sunday
                        from equipment e 
                        left join projects_booking pb on pb.equipment_id = e.id 
                        left join "analyze" a  on a.id = pb.analyse_id  
                        JOIN uuid_project y ON y.id = pb.project_id
                        where pb.is_delete = false
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by e.name, coalesce(a.analyze_name,'')
            """)
            params = {"username": user.username, "start_date": date_booking_dict['date_start'], "end_date": date_booking_dict['date_end']}

        result = await db.execute(query, params)
        rows = result.fetchall()

        df = pd.DataFrame(rows, columns=["Оборудование", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"])
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Оборудование")
        output.seek(0)

        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                 headers={"Content-Disposition": f"attachment; filename={date_booking_dict['date_start']}_{date_booking_dict['date_end']}_equipment.xlsx"})


    @staticmethod
    async def download_ratings_excel(
        request_data: InfoListsRequest,
        user,
        db: AsyncSession,
    ) -> Response:
        request_dict = request_data.dict(exclude_unset=True)
        date_booking_dict = await UserBookingService.validate_date_booking(request_dict)

        date_start = date_booking_dict["date_start"]
        date_end = date_booking_dict["date_end"]

        result = await db.execute(
            text(RATINGS_QUERY),
            {
                "date_start": date_start,
                "date_end": date_end,
            },
        )
        rows = result.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "Исполнитель",
                "Средняя оценка",
                "Без задержек",
                "Полный набор измерений",
                "Качество работы",
                "Кол-во оцененных анализов",
                "Всего завершенных анализов",
            ],
        )

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Рейтинг сотрудников")

        output.seek(0)

        filename = (
            f"{date_booking_dict['date_start']}_"
            f"{date_booking_dict['date_end']}_ratings.xlsx"
        )

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            },
        )