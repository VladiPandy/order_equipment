from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from db.postgres import get_db
from sqlalchemy import text
from typing import List

from fastapi import HTTPException, Request, Response, status
from services.wrappers import admin_only, admin_or_current_user_only
from services.info import UserInfoService
from fastapi import HTTPException, Request


from models.schemas.info import InfoProjectResponse, InfoListsRequest, \
    InfoListsResponse, InfoBookingItem


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
    if user.is_superuser:
        calback = {
            "is_admin" : 1,
            "project_name" : 'Администратор',
            "responsible_fio" : user.last_name+' '+user.first_name,
        }
    else:
        responsible_person = await db.execute(text(
            f"SELECT responsible_person,project_name FROM \"project\" WHERE project_name = '{user.username}' LIMIT 1;"))
        items = responsible_person.fetchall()
        calback = {
            "is_admin": 0,
            "project_name": items[0][1],
            "responsible_fio": items[0][0],
        }
    return calback


@router.get("/bookings",
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
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    try:
        data = await request.json()
        req_model = InfoListsRequest(**data)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    print('req_model')
    print(req_model)
    return await UserInfoService.info_bookings(req_model, user, db)


@router.get("/booking_lists",
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
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    try:
        data = await request.json()
        req_model = InfoListsRequest(**data)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    return await UserInfoService.info_booking_lists(req_model, user, db)