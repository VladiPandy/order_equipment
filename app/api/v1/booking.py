from fastapi import APIRouter,Body, Request, Response, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.schemas.booking import PossibleCreateBookingRequest, \
    PossibleCreateBookingResponse, CreateBookingResponse, \
    CreateBookingRequest, PossibleChangesResponse, PossibleChangesRequest, \
    ChangeResponse, ChangeRequest, CancelRequest, CancelResponse, \
    FeedbackResponse, FeedbackRequest
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
        # req_model: PossibleCreateBookingRequest = Body(
        #         ...,
        #         example={
        #             "date": 'None',
        #             "analyse": 'None',
        #             "equipment": 'None',
        #             "executor": 'None'
        #         }
        #     ),
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    print('user')
    try:
        body_bytes = await request.body()
        if not body_bytes:
            data = {}
        else:
            data = await request.json()
        data_check = data if data else {}
        request_model = PossibleCreateBookingRequest(**data_check)
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
        req_model: CreateBookingRequest = Body(
                        ...,
                        example={
                            "date": "21.01.2024",
                            "analyse": "Анализ 2",
                            "equipment": "Приборчик",
                            "executor": "Владилен Полосухин Дмитриевич",
                            "samples" : 19
                        }
                    ),
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
        # req_model: PossibleChangesRequest = Body(
        #                 ...,
        #                 example={
        #                     "id": 2
        #                 }
        #             ),
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
        req_model: ChangeRequest = Body(
                        ...,
                        example={
                            "id": 1,
                            "project": "Проект_1",
                            "date": "26.08.2024",
                            "analyse": "Анализ 2",
                            "equipment": "Приборчик",
                            "executor": "Владилен Полосухин Дмитриевич",
                            "samples": 1,
                            "status": "На рассмотрении",
                            "comment": "Комментарий изменения"
                        }
                    ),
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
    req_model: CancelRequest = Body(
                            ...,
                            example={
                                "id": 1
                            }
                        ),
    user: object = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        data = await request.json()
        req_model = CancelRequest(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Неверные входные данные: {e}")

    return await UserBookingService.cancel_booking(req_model,user, db)


@router.post("/feedback",
            response_model=FeedbackResponse)
@admin_or_current_user_only
async def possible_create_booking(
        request: Request,
        response: Response,
        req_model: FeedbackRequest = Body(
                ...,
                example={
                    "id": 2,
                    "question_1": True,
                    "question_2": False,
                    "question_3": False
                }
            ),
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    pass
    try:
        data = await request.json()
        req_model = FeedbackRequest(**data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Неверные входные данные: {e}")

    return await UserBookingService.feedback_booking(req_model,user, db)