from django.contrib import admin, messages

from datetime import datetime, timedelta
from .models import WorkingDayOfWeek, IsOpenRegistration, OpenWindowForOrdering, WorkerWeekStatus
from user_auth.custom_admin import custom_admin_site
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django import forms

@admin.register(WorkingDayOfWeek,site=custom_admin_site)
class WorkingDayOfWeekAdmin(admin.ModelAdmin):
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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        self.message_user(
            request,
            f"Рабочие дни недели успешно добавлены: {obj.plain_working_days()}",
            level=messages.SUCCESS
        )
        return HttpResponseRedirect(self._get_redirect_url(request, obj))

    def response_change(self, request, obj):
        self.message_user(
            request,
            f"Рабочие дни недели обновлены: {obj.plain_working_days()}",
            level=messages.SUCCESS
        )
        return HttpResponseRedirect(self._get_redirect_url(request, obj))

    def _get_redirect_url(self, request, obj):
        if "_save" in request.POST:
            request.path = request.path.replace(f"add/", "")
            return request.path.replace(f"{obj.pk}/change/", "")
        elif "_continue" in request.POST:
            return request.path.replace(f"add/", f"{obj.pk}/change/")  # останемся на той же форме
        elif "_addanother" in request.POST:
            return request.path.replace(f"{obj.pk}/change/", "add/")  # форма добавления
        else:
            return request.path # назад к списку


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
            # kwargs['choices'] = start_date_choices
            return forms.ChoiceField(
                choices=start_date_choices,
                label=db_field.verbose_name,
                help_text=db_field.help_text,
                required=not db_field.blank,
            ).formfield()
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
            # kwargs['choices'] = choices
            return forms.ChoiceField(
                choices=choices,
                label=db_field.verbose_name,
                help_text=db_field.help_text,
                required=not db_field.blank,
            ).formfield()
        return super().formfield_for_choice_field(db_field, request, **kwargs)

@admin.register(WorkerWeekStatus,site=custom_admin_site)
class WorkerWeekStatusAdmin(admin.ModelAdmin):
    pass
