from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


from django.apps import AppConfig

class CustomAuthConfig(AppConfig):
    name = 'django.contrib.auth'
    verbose_name = 'my super special auth name'

class CustomAdminSite(AdminSite):
    site_header = "Запись на анализы"  # Верхний заголовок админ-панели
    site_title = "Запись на анализы"  # Заголовок окна браузера
    index_title = "Добро пожаловать в Запись на анализы"

    def has_permission(self, request):
        # Разрешаем доступ только если пользователь авторизован и is_staff=True
        return request.user.is_authenticated and request.user.is_staff

    def index(self, request, extra_context=None):
        # Если пользователь аутентифицирован, но не является staff, перенаправляем его на главную страницу
        if request.user.is_authenticated and not request.user.is_staff:
            return HttpResponseRedirect(reverse('home'))
        return super().index(request, extra_context)

custom_admin_site = CustomAdminSite(name= 'admin')

custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)