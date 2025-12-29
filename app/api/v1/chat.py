import logging
from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from db.postgres import get_db
from services.wrappers import admin_or_current_user_only
from models.schemas.chat import ChatMessageResponse, ChatMessageCreate
from sql.chat_queries import (
    GET_BOOKING_MESSAGES_QUERY,
    INSERT_BOOKING_MESSAGE_QUERY,
)
from sql.info_queries import PROJECT_INFO_QUERY

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/booking/messages/{booking_id}",
    response_model=List[ChatMessageResponse],
    tags=["Чат"],
    summary="Получить диалог по бронированию",
    description="Возвращает список сообщений чата по конкретному бронированию",
    response_description="Список сообщений",
    status_code=status.HTTP_200_OK,
)
@admin_or_current_user_only
async def get_booking_messages(
    booking_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: object = None,
):
    try:
        result = await db.execute(
            text(GET_BOOKING_MESSAGES_QUERY),
            {
                "booking_id": booking_id,
                "current_username": user.username,
            },
        )
        rows = result.mappings().all()
        return rows

    except Exception as e:
        logger.exception("Ошибка получения сообщений чата")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения сообщений: {e}",
        )


@router.post(
    "/booking/messages/{booking_id}",
    response_model=ChatMessageResponse,
    tags=["Чат"],
    summary="Отправить сообщение в чат",
    description="Создает новое сообщение в диалоге бронирования",
    response_description="Созданное сообщение",
    status_code=status.HTTP_201_CREATED,
)
@admin_or_current_user_only
async def create_booking_message(
    booking_id: int,
    request: Request,
    body: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
    user: object = None,
):
    responsible_person = await db.execute(text(
        PROJECT_INFO_QUERY.format(username=user.username)))
    items = responsible_person.fetchall()
    try:
        result = await db.execute(
            text(INSERT_BOOKING_MESSAGE_QUERY),
            {
                "booking_id": booking_id,
                "author": items[0][1] if items else 'Admin',
                "author_username": user.username,
                "is_admin": bool(items[0][3]) if items else True,
                "message": body.message,
            },
        )
        await db.commit()

        row = result.mappings().first()
        if not row:
            raise HTTPException(
                status_code=500,
                detail="Сообщение не было создано",
            )

        return row

    except Exception as e:
        await db.rollback()
        logger.exception("Ошибка создания сообщения чата")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка отправки сообщения: {e}",
        )
