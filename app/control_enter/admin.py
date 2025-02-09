from django.contrib import admin

from .models import WorkingDayOfWeek, IsOpenRegistration, OpenWindowForOrdering, WorkerWeekStatus
from user_auth.custom_admin import custom_admin_site

@admin.register(WorkingDayOfWeek,site=custom_admin_site)
class WorkingDayOfWeekAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        """
        Запрещаем добавление новой записи, если уже существует одна запись
        """
        if WorkingDayOfWeek.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def get_model_perms(self, request):
        """
        Возвращает права доступа к модели. Здесь мы ограничиваем возможность добавления новой записи,
        оставляя только редактирование и просмотр.
        """
        perms = super().get_model_perms(request)
        # Блокируем возможность добавления новой записи, если уже есть одна запись
        if WorkingDayOfWeek.objects.count() >= 1:
            perms['add'] = False
        return perms

@admin.register(IsOpenRegistration,site=custom_admin_site)
class IsOpenRegistrationAdmin(admin.ModelAdmin):
    pass

@admin.register(OpenWindowForOrdering,site=custom_admin_site)
class OpenWindowForOrderingAdmin(admin.ModelAdmin):
    pass

@admin.register(WorkerWeekStatus,site=custom_admin_site)
class WorkerWeekStatusAdmin(admin.ModelAdmin):
    pass
