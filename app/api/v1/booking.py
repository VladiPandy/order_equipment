from fastapi import APIRouter, Body, Request, Response, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from models.schemas.booking import PossibleCreateBookingRequest, \
    PossibleCreateBookingResponse, CreateBookingResponse, \
    CreateBookingRequest, PossibleChangesResponse, PossibleChangesRequest, \
    ChangeResponse, ChangeRequest, CancelRequest, CancelResponse, \
    FeedbackResponse, FeedbackRequest
from services.booking import UserBookingService
from db.postgres import get_db

from services.wrappers import admin_only, admin_or_current_user_only

# Настройка логгера
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/possible_create",
            response_model=PossibleCreateBookingResponse)
@admin_or_current_user_only
async def possible_create_booking(
        request: Request,
        response: Response,
        req_model: PossibleCreateBookingRequest ,
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
        request_model = PossibleCreateBookingRequest(**data_check)
        logger.info(f"Получен запрос на возможное создание бронирования: {data_check}")
    except Exception as e:
        logger.error(f"Ошибка валидации входных данных: {str(e)}")
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    cookie_createkey = request.cookies.get("createkey")
    logger.debug(f"Cookie createkey: {cookie_createkey}")
    
    # try:
    result = await UserBookingService.get_possible_create_booking(
        request_data=request_model,
        response=response,
        db=db,
        user=user,
        cookie_createkey=cookie_createkey
    )
    logger.info(f"Успешно получены возможные варианты бронирования")
    return result
    # except Exception as e:
    #     logger.error(f"Ошибка при получении возможных вариантов бронирования: {str(e)}")
    #     raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")



@router.post('/create',
            response_model=CreateBookingResponse
)
@admin_or_current_user_only
async def create_booking_row(
        request: Request,
        response: Response,
        req_model: CreateBookingRequest ,
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    try:
        data = await request.json()
        logger.info(f"Получен запрос на создание бронирования: {data}")
        request_model = CreateBookingRequest(**data)
    except Exception as e:
        logger.error(f"Ошибка валидации входных данных: {str(e)}")
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    cookie_createkey = request.cookies.get("createkey")
    logger.debug(f"Cookie createkey: {cookie_createkey}")
    
    # try:
    id_create = await UserBookingService.create_booking(
        request_data=request_model,
        response=response,
        db=db,
        user=user,
        cookie_createkey=cookie_createkey
    )
    logger.info(f"Успешно создано бронирование с ID: {id_create}")
    return {
        "id": id_create
    }
    # except Exception as e:
    #     logger.error(f"Ошибка при создании бронирования: {str(e)}")
    #     raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/possible_changes", response_model=PossibleChangesResponse)
@admin_or_current_user_only
async def get_possible_changes(
        request: Request,
        req_model: PossibleChangesRequest,
        user: object = None,
        db: AsyncSession = Depends(get_db)
):
    try:
        data = await request.json()
        req_model = PossibleChangesRequest(**data)
        logger.info(f"Получен запрос на возможные изменения бронирования: {data}")
    except Exception as e:
        logger.error(f"Ошибка валидации входных данных: {str(e)}")
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    # try:
    #     # Получаем данные о бронировании
    result = await UserBookingService.get_possible_changes(req_model, user, db)
    logger.info(f"Успешно получены возможные варианты изменения бронирования")
    return result
    # except Exception as e:
    #     logger.error(f"Ошибка при получении возможных изменений: {str(e)}")
    #     raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")



@router.post("/change", response_model=ChangeResponse)
@admin_or_current_user_only
async def change_booking(
        request: Request,
        req_model: ChangeRequest,
        user: object = None,
        db: AsyncSession = Depends(get_db)
):
    try:
        data = await request.json()
        logger.info(f"Получен запрос на изменение бронирования: {data}")
        req_model = ChangeRequest(**data)
    except Exception as e:
        logger.error(f"Ошибка валидации входных данных: {str(e)}")
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    # try:
    result = await UserBookingService.change_booking(req_model, user, db)
    logger.info(f"Успешно изменено бронирование")
    return result
    # except Exception as e:
    #     logger.error(f"Ошибка при изменении бронирования: {str(e)}")
    #     raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.delete("/cancel", response_model=CancelResponse)
@admin_or_current_user_only
async def cancel_booking(
    request: Request,
    req_model: CancelRequest,
    user: object = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        data = await request.json()
        logger.info(f"Получен запрос на отмену бронирования: {data}")
        req_model = CancelRequest(**data)
    except Exception as e:
        logger.error(f"Ошибка валидации входных данных: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Неверные входные данные: {e}")

    # try:
    result = await UserBookingService.cancel_booking(req_model, user, db)
    logger.info(f"Успешно отменено бронирование")
    return result
    # except Exception as e:
    #     logger.error(f"Ошибка при отмене бронирования: {str(e)}")
    #     raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/feedback",
            response_model=FeedbackResponse)
@admin_or_current_user_only
async def feedback_booking(
        request: Request,
        req_model: FeedbackRequest,
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    try:
        data = await request.json()
        logger.info(f"Получен запрос на отправку обратной связи: {data}")
        req_model = FeedbackRequest(**data)
    except Exception as e:
        logger.error(f"Ошибка валидации входных данных: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Неверные входные данные: {e}")

    # try:
    result = await UserBookingService.feedback_booking(req_model, user, db)
    logger.info(f"Успешно отправлена обратная связь")
    return result
    # except Exception as e:
    #     logger.error(f"Ошибка при отправке обратной связи: {str(e)}")
    #     raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")