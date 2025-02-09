import datetime
from datetime import timedelta
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from typing import Dict, List, Any

from models.schemas.info import InfoProjectResponse, InfoListsRequest, \
    InfoListsResponse, InfoBookingItem
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
                    SELECT id, project_name FROM "project" WHERE project_name = :username
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
                projects=[],
                date_bookings=[],
                analyzes=[],
                equipments=[],
                executors=[],
                statuses=[]
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
            projects=projects,
            date_bookings=list(date_bookings_set),
            analyzes=list(analyzes_set),
            equipments=list(equipments_set),
            executors=list(executors_set),
            statuses=list(statuses_set)
        )

    @staticmethod
    async def info_bookings(
            request_data: InfoListsRequest,
            user,
            db: AsyncSession,
    ) -> InfoBookingItem:
        # 1. Парсинг даты
        request_dict = request_data.dict(exclude_unset=True)

        date_booking_dict = await UserBookingService.validate_date_booking(
            request_dict)

        print(date_booking_dict)

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
                        SELECT id, project_name FROM "project" WHERE project_name = :username
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

        print('rows')
        print(rows)

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
                date_booking=date_booking_str,
                analyze=row[3],
                equipment=row[4],
                executor=row[5],
                count_samples=row[6],
                status=row[7],
                comment=row[8] if row[8] is not None else ""
            )
            bookings.append(booking_item)

        return bookings
