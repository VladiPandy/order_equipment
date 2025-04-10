from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from db.postgres import get_db
from sqlalchemy import text
from typing import List
import logging

from fastapi import  APIRouter, Body, HTTPException, Request, Response, status
from services.wrappers import admin_only, admin_or_current_user_only
from services.info import UserInfoService
from fastapi import HTTPException, Request
from datetime import datetime
from sql.info_queries import PROJECT_INFO_QUERY, OPEN_GLOBAL_WINDOW_QUERY, OPEN_LOCAL_REGISTRATION_QUERY

from models.schemas.info import InfoProjectResponse, InfoListsRequest, \
    InfoListsResponse, InfoBookingItem, InfoExecutorTable, InfoEquipmentTable

# Настройка логгера
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/project",
    response_model=InfoProjectResponse,
    tags=['Информация'],
    summary='Информация о пользователе',
    description='Краткая информация о пользователе для разграничения контента',
    response_description='Пользователь успешно найден',
    status_code=status.HTTP_200_OK
)
@admin_or_current_user_only
async def possible_create_booking(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    responsible_person = await db.execute(text(
        PROJECT_INFO_QUERY.format(username=user.username)))
    items = responsible_person.fetchall()
    if user.is_superuser:
        if not items:
            calback = {
                "is_admin" : 1,
                "project_name" : 'Администратор',
                "responsible_fio" : 'admin',
                "is_open" : False
            }
        else:
            calback = {
                "is_admin": 1,
                "project_name": f'Администратор',
                "responsible_fio": items[0][0],
                "is_open": False
            }
    else:
        today = datetime.today()
        date_str = today.strftime('%d.%m.%Y')
        time_str = today.strftime('%H:%M')
        is_open_global = await db.execute(text(
            OPEN_GLOBAL_WINDOW_QUERY.format(date_str=date_str, time_str=time_str, is_priority=items[0][2])))
        is_open_items = is_open_global.fetchall()
        if not is_open_items:
            is_open_local = await db.execute(text(
                OPEN_LOCAL_REGISTRATION_QUERY))
            is_open_l_items= is_open_local.fetchall()
            logger.debug(f"Найдены записи isopenregistration: {is_open_l_items}")
        else:
            is_open_l_items = None
        status_open = 1 if is_open_l_items or is_open_items else 0

        calback = {
            "is_admin": 0,
            "project_name": items[0][1],
            "responsible_fio": items[0][0],
            "is_open": status_open
        }
    return calback


@router.post("/bookings",
    response_model = List[InfoBookingItem],
    tags = ['Информация'],
    summary = 'Получение таблицы броней',
    description = 'Получение всей информации о времени бронирования',
    response_description = 'Список записей на бронирование',
    status_code = status.HTTP_200_OK
)
@admin_or_current_user_only
async def get_project_bookings(
        request: Request,
        req_model: InfoListsRequest ,
        db: AsyncSession = Depends(get_db),
        user: object = None
) -> InfoListsRequest:
    try:
        body_bytes = await request.body()
        if not body_bytes:
            data = {}
        else:
            data = await request.json()
        data_check = data if data else {}
        req_model = InfoListsRequest(**data_check)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    return await UserInfoService.info_bookings(req_model, user, db)


@router.post("/booking_lists",
    response_model=InfoListsResponse,
    tags=['Информация'],
    summary='Списки для фильтрации',
    description='Списки для фильтрации выводимой информации по бронированию',
    response_description='Успешно найдены списки для фильтрации',
    status_code=status.HTTP_200_OK
)
@admin_or_current_user_only
async def get_project_bookings(
        request: Request,
        req_model: InfoListsRequest ,
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    try:
        body_bytes = await request.body()
        if not body_bytes:
            data = {}
        else:
            data = await request.json()
        data_check = data if data else {}
        req_model = InfoListsRequest(**data_check)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    return await UserInfoService.info_booking_lists(req_model, user, db)


@router.post("/table_executor",
    response_model = List[InfoExecutorTable],
    tags = ['Информация'],
    summary = 'Получение таблицы исполнителей',
    description = 'Получение всей информации о времени бронирования исполнителями',
    response_description = 'Список записей занятости исполнителей',
    status_code = status.HTTP_200_OK
)
@admin_or_current_user_only
async def get_project_bookings(
        request: Request,
        req_model: InfoListsRequest ,
        db: AsyncSession = Depends(get_db),
        user: object = None
) -> InfoListsRequest:
    try:
        body_bytes = await request.body()
        if not body_bytes:
            data = {}
        else:
            data = await request.json()
        data_check = data if data else {}
        req_model = InfoListsRequest(**data_check)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    return await UserInfoService.info_executor(req_model, user, db)


@router.post("/table_equipment",
    response_model = List[InfoEquipmentTable],
    tags = ['Информация'],
    summary = 'Получение таблицы исполнителей',
    description = 'Получение всей информации о времени бронирования исполнителями',
    response_description = 'Список записей занятости исполнителей',
    status_code = status.HTTP_200_OK
)
@admin_or_current_user_only
async def get_project_bookings(
        request: Request,
        req_model: InfoListsRequest ,
        db: AsyncSession = Depends(get_db),
        user: object = None
) -> InfoListsRequest:
    try:
        body_bytes = await request.body()
        if not body_bytes:
            data = {}
        else:
            data = await request.json()
        data_check = data if data else {}
        req_model = InfoListsRequest(**data_check)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    return await UserInfoService.info_equipment(req_model, user, db)