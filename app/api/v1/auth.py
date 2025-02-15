from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from db.postgres import get_db
from fastapi import  APIRouter, Body, HTTPException, Request, Response, status
from services.wrappers import admin_only, admin_or_current_user_only, check_auth
from fastapi import HTTPException, Request

router = APIRouter()

@router.get("/auth_check",
)
@check_auth
async def auth_check(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user: object = None
):
    print(user)
    if not user or not getattr(user, 'is_authenticated', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")
    return Response("Authorized", status_code=status.HTTP_200_OK)