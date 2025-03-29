from django.contrib import admin

from datetime import datetime, timedelta
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
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "week_period":
            # Получаем текущую дату
            today = datetime.today()
            # Находим понедельник текущей недели
            monday = today - timedelta(days=today.weekday())
            # Формируем список периодов на ближайшие 3 недели
            week_period_choices = []
            for i in range(3):
                week_start = monday + timedelta(weeks=i)
                week_end = week_start + timedelta(days=6)
                period = f"{week_start.strftime('%d.%m.%Y')} - {week_end.strftime('%d.%m.%Y')}"
                week_period_choices.append((period, period))
            kwargs['choices'] = week_period_choices
        return super().formfield_for_choice_field(db_field, request, **kwargs)

@admin.register(OpenWindowForOrdering,site=custom_admin_site)
class OpenWindowForOrderingAdmin(admin.ModelAdmin):
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "start_date":
            start_date_choices = [
                ((datetime.today() + timedelta(days=i)).strftime('%d.%m.%Y'),
                 (datetime.today() + timedelta(days=i)).strftime('%d.%m.%Y'))
                for i in range(0, 21)
            ]
            kwargs['choices'] = start_date_choices
        return super().formfield_for_choice_field(db_field, request, **kwargs)

@admin.register(WorkerWeekStatus,site=custom_admin_site)
class WorkerWeekStatusAdmin(admin.ModelAdmin):
    pass
