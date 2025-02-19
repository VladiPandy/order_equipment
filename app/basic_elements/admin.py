from django.contrib import admin

from .models import Equipment, Analyze, Executor, Project, AnalyzeType
# from .models import (Analyze, Equipment, Operator, Project, WorkingDayOfWeek, IsWorkingDay, Status,
#                      AnalyzePerEquipment, OperatorPerEquipment, OperatorPerWeek, ProjectPerAnalyze,
#                      ProjectOrderingEquipment, OpenWindowForOrdering, IsOpenRegistration)

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from user_auth.custom_admin import custom_admin_site
from django.contrib.auth.models import User, Group

from django.contrib import admin

admin.site.site_header = _("Администратор сервиса бронирования")
admin.site.site_title = _("Администрирование сервиса бронирования")
admin.site.index_title = _("Добро пожаловать в панель управления")

admin.site.unregister(User)
admin.site.unregister(Group)
custom_admin_site.unregister(User)
custom_admin_site.unregister(Group)

@admin.register(AnalyzeType,site=custom_admin_site)
class EquipmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Equipment,site=custom_admin_site)
class EquipmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Analyze,site=custom_admin_site)
class AnalyzeAdmin(admin.ModelAdmin):
    pass

@admin.register(Executor,site=custom_admin_site)
class ExecutorAdmin(admin.ModelAdmin):
    pass

@admin.register(Project,site=custom_admin_site)
class ProjectAdmin(admin.ModelAdmin):
    pass
