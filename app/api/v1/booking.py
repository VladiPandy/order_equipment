from fastapi import APIRouter, Request, Response, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.schemas.booking import PossibleCreateBookingRequest, \
    PossibleCreateBookingResponse, CreateBookingResponse, \
    CreateBookingRequest, PossibleChangesResponse, PossibleChangesRequest, \
    ChangeResponse, ChangeRequest, CancelRequest, CancelResponse
from services.booking import UserBookingService
from db.postgres import get_db

from services.wrappers import admin_only, admin_or_current_user_only

router = APIRouter()


@router.get("/possible_create",
            response_model=PossibleCreateBookingResponse)
@admin_or_current_user_only
async def possible_create_booking(
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    data = await request.json()
    print(user)
    try:
        request_model = PossibleCreateBookingRequest(**data)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    cookie_createkey = request.cookies.get("createkey")

    result = await UserBookingService.get_possible_create_booking(
        request_data=request_model,
        response=response,
        db=db,
        user=user,
        cookie_createkey=cookie_createkey
    )

    return result



@router.post('/create',
            response_model=CreateBookingResponse
)
@admin_or_current_user_only
async def create_booking_row(
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    data = await request.json()
    print(data)
    try:
        request_model = CreateBookingRequest(**data)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    cookie_createkey = request.cookies.get("createkey")
    print(user)
    id_create = await  UserBookingService.create_booking(
        request_data=request_model,
        response=response,
        db=db,
        user=user,
        cookie_createkey=cookie_createkey
    )

    return {
        "id": id_create
    }


@router.get("/possible_changes", response_model=PossibleChangesResponse)
@admin_or_current_user_only
async def get_possible_changes(
        request: Request,
        user: object = None,
        db: AsyncSession = Depends(get_db)
):
    try:
        data = await request.json()
        req_model = PossibleChangesRequest(**data)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    print(req_model)
    return await UserBookingService.get_possible_changes(req_model,user, db)



@router.post("/change", response_model=ChangeResponse)
@admin_or_current_user_only
async def change_booking(
        request: Request,
        user: object = None,
        db: AsyncSession = Depends(get_db)
):
    data = await request.json()
    try:
        req_model = ChangeRequest(**data)
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Неверные входные данные: {e}")

    return await UserBookingService.change_booking(req_model,user, db)


@router.delete("/cancel", response_model=CancelResponse)
@admin_or_current_user_only
async def cancel_booking(
    request: Request,
    user: object = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        data = await request.json()
        req_model = CancelRequest(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Неверные входные данные: {e}")

    return await UserBookingService.cancel_booking(req_model,user, db)