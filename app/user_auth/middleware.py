# basic_elements/middleware.py

from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """
    Middleware, которое требует авторизацию для всех запросов, за исключением заданных URL.

    Логика:
    - Если пользователь не аутентифицирован и запрашиваемый URL не входит в список исключений,
      происходит перенаправление на страницу логина (адрес задаётся в settings.LOGIN_URL).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # URL, которые не требуют авторизации (например, страница логина, регистрации, статика и т.п.)
        self.exempt_urls = [settings.LOGIN_URL]
        # Если у вас в настройках указаны дополнительные исключения, добавьте их
        if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
            self.exempt_urls.extend(settings.LOGIN_EXEMPT_URLS)

    def __call__(self, request):
        # Если пользователь не аутентифицирован
        if not request.user.is_authenticated:
            # И запрашиваемый URL не входит в список исключений
            if not any(
                    request.path.startswith(url) for url in self.exempt_urls):
                return redirect(settings.LOGIN_URL)
        # Иначе продолжаем обработку запроса
        response = self.get_response(request)
        return response