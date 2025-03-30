import datetime
from datetime import timedelta
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from typing import Dict, List, Any

from models.schemas.info import InfoProjectResponse, InfoListsRequest, \
    InfoListsResponse, InfoBookingItem, InfoEquipmentTable, InfoExecutorTable
from services.booking import UserBookingService

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

        print(date_booking_dict)

        #Формируем запрос в зависимости от роли пользователя

        if user.is_staff:
            query = text("""
                SELECT y.project_name, x.date_booking, z.analyze_name, e.name, concat(ex.first_name,' ',ex.last_name,' ',ex.patronymic), x.status
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
                SELECT y.project_name, x.date_booking, z.analyze_name, e.name, concat(ex.first_name,' ',ex.last_name,' ',ex.patronymic), x.status
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
        print(projects_set)
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
        print(request_dict)
        date_booking_dict = await UserBookingService.validate_date_booking(
            request_dict)


        # Формируем запрос в зависимости от роли пользователя

        if user.is_staff:
            query = text("""
                    SELECT x.id, y.project_name, x.date_booking, z.analyze_name, e.name
                     , concat(ex.first_name,' ',ex.last_name,' ',ex.patronymic),x.count_analyses, x.status, x.comment
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
                    SELECT x.id, y.project_name, x.date_booking, z.analyze_name, e.name
                        , concat(ex.first_name,' ',ex.last_name,' ',ex.patronymic), x.count_analyses, x.status, x.comment
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

        if not rows:
            return []  # Возвращаем пустой список, если данных нет

        bookings: List[InfoBookingItem] = []
        for row in rows:
            # row: (id, project, date_booking, analyze, equipment, executor, count_samples, status, comment)
            print(row)
            try:
                date_booking_str = row[2].strftime("%d.%m.%Y") if row[2] else ""
            except Exception:
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
                comment=row[8] if row[8] is not None else ""
            )
            bookings.append(booking_item)

        return bookings


    @staticmethod
    async def info_executor(
            request_data: InfoListsRequest,
            user,
            db: AsyncSession,
    ) -> InfoBookingItem:
        # 1. Парсинг даты
        request_dict = request_data.dict(exclude_unset=True)
        print(request_dict)
        date_booking_dict = await UserBookingService.validate_date_booking(
            request_dict)

        # Формируем запрос в зависимости от роли пользователя

        if user.is_staff:
            query = text("""
                        select concat(e.first_name,e.last_name,coalesce(e.patronymic,'')) fio
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
                        where pb.is_delete = false
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by concat(e.first_name,e.last_name,coalesce(e.patronymic,'')), coalesce(a.analyze_name,'')
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

        if not rows:
            return []  # Возвращаем пустой список, если данных нет

        bookings = []
        for row in rows:
            # row: (id, project, date_booking, analyze, equipment, executor, count_samples, status, comment)
            print(row)

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
        print(bookings)
        return bookings



    @staticmethod
    async def info_equipment(
            request_data: InfoListsRequest,
            user,
            db: AsyncSession,
    ) -> InfoBookingItem:
        # 1. Парсинг даты
        request_dict = request_data.dict(exclude_unset=True)
        print(request_dict)
        date_booking_dict = await UserBookingService.validate_date_booking(
            request_dict)

        # Формируем запрос в зависимости от роли пользователя

        if user.is_staff:
            query = text("""
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
                        where pb.is_delete = false
                        and pb.date_booking BETWEEN :start_date AND :end_date
                        group by e.name, coalesce(a.analyze_name,'')
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

        if not rows:
            return []  # Возвращаем пустой список, если данных нет

        bookings = []
        for row in rows:
            # row: (id, project, date_booking, analyze, equipment, executor, count_samples, status, comment)
            print(row)

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
        print(bookings)
        return bookings

