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
            return user
        except User.DoesNotExist:
            return None

    auth_header = request.headers.get("Authorization")
    print(auth_header)
    if auth_header and auth_header.startswith("Basic "):
        print(auth_header.split(" ")[1])
        try:
            # Извлекаем и декодируем учетные данные
            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = b64decode(encoded_credentials).decode("utf-8")
            username, password = decoded_credentials.split(":", 1)
        except Exception:
            return None
        user = authenticate(username=username, password=password)
        print(user)
        return user



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

        print(db_async_session)
        # Получаем пользователя из Django-сессии
        user = await get_django_user_from_request(request, db_async_session)
        print(user)
        if not user:
            print('here ')
            login_url = getattr(settings, 'LOGIN_URL', '/login/')
            return RedirectResponse(url=f"http://127.0.0.1/{login_url}?next=http://127.0.0.1/{request.url.path}", status_code=303)
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Пользователь не аутентифицирован"
            # )

        # Проверяем, что пользователь является администратором
        if not user.is_superuser:
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
            print('here ')
            login_url = getattr(settings, 'LOGIN_URL', '/login/')
            return RedirectResponse(
                url=f"http://127.0.0.1{login_url}?next=http://127.0.0.1:{request.url.path}",
                status_code=303)
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Пользователь не аутентифицирован"
            # )

        # Если пользователь является администратором или его id совпадает с запрашиваемым
        kwargs['user'] = user
        return await func(*args, **kwargs)

    return wrapper