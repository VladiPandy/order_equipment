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
            today = datetime.today()
            # Определяем понедельник текущей недели.
            current_monday = today - timedelta(days=today.weekday())
            choices = [
                (
                    (current_monday + timedelta(days=i * 7)).strftime('%d.%m.%Y') + '-' +
                    (current_monday + timedelta(days=i * 7 + 6)).strftime('%d.%m.%Y'),
                    (current_monday + timedelta(days=i * 7)).strftime('%d.%m.%Y') + '-' +
                    (current_monday + timedelta(days=i * 7 + 6)).strftime('%d.%m.%Y')
                )
                for i in range(12)
            ]
            kwargs['choices'] = choices
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
        if db_field.name == "week_period":
            today = datetime.today()
            # Определяем понедельник текущей недели.
            current_monday = today - timedelta(days=today.weekday())
            choices = [
                (
                    (current_monday + timedelta(days=i * 7)).strftime('%d.%m.%Y') + '-' +
                    (current_monday + timedelta(days=i * 7 + 6)).strftime('%d.%m.%Y'),
                    (current_monday + timedelta(days=i * 7)).strftime('%d.%m.%Y') + '-' +
                    (current_monday + timedelta(days=i * 7 + 6)).strftime('%d.%m.%Y')
                )
                for i in range(12)
            ]
            kwargs['choices'] = choices
        return super().formfield_for_choice_field(db_field, request, **kwargs)

@admin.register(WorkerWeekStatus,site=custom_admin_site)
class WorkerWeekStatusAdmin(admin.ModelAdmin):
    pass
