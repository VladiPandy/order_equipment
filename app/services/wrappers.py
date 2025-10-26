from functools import wraps
from base64 import b64decode
from fastapi import HTTPException, Request
from db.postgres import get_db
from starlette import status
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model, authenticate
from django.contrib.sessions.backends.db import SessionStore
from starlette.responses import RedirectResponse
from django.conf import settings
import logging
from django.contrib.auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession
import base64

from dependings.models import Project, Adminstrator

logger = logging.getLogger(__name__)

@sync_to_async
def get_django_user_from_request(request: Request, db_async_session):
    """
    Функция, которая пытается извлечь пользователя из Django-сессии на основе cookies.

    Входные параметры:
    - request: Request - объект запроса FastAPI.

    Выходные данные:
    - Объект пользователя (User) или None, если пользователь не авторизован.
    """

    session_id = request.cookies.get('sessionid')

    if session_id:
        # Инициализируем Django SessionStore по session_key
        s = SessionStore(session_key=session_id)
        try:
            # Попытка загрузить сессию из БД
            s.load()
        except Exception:
            # Если сессия невалидна или отсутствует
            return None
        user_id = s.get('_auth_user_id')
        if not user_id:
            return None

        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
            user.user_type = 'web'
            return user
        except User.DoesNotExist:
            return None

    auth_header = request.headers.get("Authorization")
    logger.debug(f"Authorization header: {auth_header}")
    if auth_header and auth_header.startswith("Basic "):
        logger.debug(f"Basic auth token: {auth_header.split(' ')[1]}")
        try:
            # Извлекаем и декодируем учетные данные
            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = b64decode(encoded_credentials).decode("utf-8")
            logger.debug(f"Decoded credentials: {decoded_credentials}")
            username, password = decoded_credentials.split(":", 1)
        except Exception as e:
            logger.error(f"Error decoding credentials: {str(e)}")
            return None
        user = authenticate(username=username, password=password)
        user.user_type = 'web'
        logger.info(f"Authenticated user: {user}")
        return user

    telegram_secret = request.headers.get("X-Telegram-Secret")
    telegram_nick = request.headers.get("X-Telegram-Nick")

    if telegram_secret and telegram_nick:
        expected_secret = getattr(settings, "TELEGRAM_SHARED_SECRET", None)
        if not expected_secret or telegram_secret != expected_secret:
            logger.warning("Invalid TELEGRAM_SHARED_SECRET in request")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Telegram secret"
            )

        # Нормализуем ник
        clean_nick = telegram_nick.strip().lstrip('@')

        try:
            project = Project.objects.filter(telegram_nick=clean_nick).first()
            adminstrator = Adminstrator.objects.filter(telegram_nick=clean_nick).first()
            if project:
                logger.info(f"Telegram auth success for project {project.project_nick}")
                user = authenticate(username=project.project_nick, password=project.project_password)
                user.user_type = 'telegram'
                return user
            elif adminstrator:
                logger.info(f"Telegram auth success for adminstrator {adminstrator.admin_nick}")
                user = authenticate(username=adminstrator.admin_nick, password=adminstrator.admin_password)
                user.user_type = 'telegram'
                return user
            else:
                logger.warning(f"Telegram nick not found: {clean_nick}")
        except Exception as e:
            logger.error(f"Telegram auth DB lookup failed: {e}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ник телеграмма не авторизован"
        )

    return None


def check_auth(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Извлекаем объект запроса и асинхронную сессию из именованных аргументов
        request: Request = kwargs.get('request')
        db_async_session: AsyncSession = kwargs.get('db_async_session')

        logger.debug(f"DB async session: {db_async_session}")
        # Получаем пользователя из Django-сессии
        user = await get_django_user_from_request(request, db_async_session)

        kwargs['user'] = user

        return await func(*args, **kwargs)
    return wrapper

def admin_only(func):
    """
    Декоратор для доступа, разрешённого только администраторам.

    Логика:
    - Извлекает пользователя из Django-сессии.
    - Если пользователь не аутентифицирован или не является администратором (is_superuser != True),
      выбрасывается HTTPException с кодом 403.
    - Иначе вызывается оригинальная функция.

    Аргументы:
        func (Callable): функция-эндпоинт, которая должна принимать в параметрах request и db_async_session.

    Возвращает:
        Callable: обёртку функции с проверкой прав доступа.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Извлекаем объект запроса и асинхронную сессию из именованных аргументов
        request: Request = kwargs.get('request')
        db_async_session: AsyncSession = kwargs.get('db_async_session')

        logger.debug(f"DB async session: {db_async_session}")
        # Получаем пользователя из Django-сессии
        user = await get_django_user_from_request(request, db_async_session)
        logger.debug(f"User: {user}")
        if not user:
            logger.info("User not authenticated, redirecting to login page")
            login_url = getattr(settings, 'LOGIN_URL', '/login/')
            return RedirectResponse(url=f"http://127.0.0.1/{login_url}?next=http://127.0.0.1/{request.url.path}", status_code=303)
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Пользователь не аутентифицирован"
            # )

        # Проверяем, что пользователь является администратором
        if not user.is_superuser:
            logger.warning(f"User {user.username} is not an admin")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для доступа"
            )

        return await func(*args, **kwargs)

    return wrapper


def admin_or_current_user_only(func):
    """
    Декоратор для доступа, разрешённого либо администраторам, либо пользователю,
    чей идентификатор совпадает с запрашиваемым.

    Логика:
    - Извлекает пользователя из Django-сессии.
    - Если пользователь не аутентифицирован – выбрасывается 401.
    - Если пользователь является администратором (is_superuser == True) или
      его id совпадает с id, переданным в параметрах (user_id), то доступ разрешается.
    - Иначе – выбрасывается HTTPException с кодом 403.

    Аргументы:
        func (Callable): функция-эндпоинт, которая должна принимать в параметрах request,
                         db_async_session и user_id.

    Возвращает:
        Callable: обёртку функции с проверкой прав доступа.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Извлекаем необходимые объекты из именованных аргументов
        request: Request = kwargs.get('request')
        db_async_session: AsyncSession = kwargs.get('db_async_session')
        # Идентификатор пользователя, для которого запрашивается доступ
        target_user_id: str = kwargs.get('user_id')

        # Получаем пользователя из Django-сессии
        user = await get_django_user_from_request(request, db_async_session)
        if not user:
            logger.info("User not authenticated, redirecting to login page")
            login_url = getattr(settings, 'LOGIN_URL', '/login/')
            return RedirectResponse(
                url=f"http://80.209.240.64{login_url}?next=http://80.209.240.64:{request.url.path}",
                status_code=303)
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Пользователь не аутентифицирован"
            # )

        # Если пользователь является администратором или его id совпадает с запрашиваемым
        kwargs['user'] = user
        return await func(*args, **kwargs)

    return wrapper