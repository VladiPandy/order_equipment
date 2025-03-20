import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
import django


from api.v1 import info, booking, auth
from db import postgres

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

async_engine = None
AsyncSessionLocal = None

async def lifespan(app: FastAPI):
    database_url = (
        f"postgresql+asyncpg://{'DB_USER'}:"
        f"{'DB_PASSWORD'}@{'80.209.240.64'}:"
        f"{'5442'}/{'DB_NAME'}"
    )

    # Создаем асинхронный движок
    async_engine = create_async_engine(
        database_url,
        future=True,
        echo=False,  # Включите True для логирования SQL-запросов
    )

    # Создаем фабрику сессий
    postgres.db_session_factory = sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    yield
    await async_engine.dispose()


app = FastAPI(
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5174"],  # или список разрешённых доменов, например, ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(info.router, prefix='/api/v1/info', tags=['Информация'])
app.include_router(booking.router, prefix='/api/v1/booking', tags=['Бронирование'])
app.include_router(auth.router, prefix='/api/v1/auth', tags=['Авторизация'])

if __name__ == '__main__':
    uvicorn.run(
        'fastapi_app:app',
        host='0.0.0.0',
        port=8001,
    )