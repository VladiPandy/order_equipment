from django.contrib import admin

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from user_auth.custom_admin import custom_admin_site

admin.site.site_header = "Администратор сервиса бронирования"
admin.site.site_title = "Администрирование сервиса бронирования"
admin.site.index_title = "Добро пожаловать в панель управления"

urlpatterns = [
    #Используем кастомный админ-сайт; при входе в /admin/ пользователи без прав будут перенаправлены на главную
    path('admin/', custom_admin_site.urls),

    #Путь для логина
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    #Путь для логаута
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    # Главная страница
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
