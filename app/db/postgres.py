from typing import AsyncGenerator
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

db_session_factory: Union[sessionmaker, None] = None

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронная зависимость для получения сессии к базе данных PostgreSQL.
    Здесь мы используем глобальную фабрику сессий для создания новой сессии на каждый запрос.
    """
    if db_session_factory is None:
        raise RuntimeError("DB session factory is not initialized. Check if lifespan is configured correctly.")

    async with db_session_factory() as session:
        yield session