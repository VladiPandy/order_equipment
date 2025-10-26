from django.contrib import admin
from .models import *
# Register your models here.
from user_auth.custom_admin import custom_admin_site

@admin.register(ProjectPerAnalyze,site=custom_admin_site)
class ProjectPerAnalyzeAdmin(admin.ModelAdmin):     
    pass

@admin.register(OperatorPerEquipment,site=custom_admin_site)
class OperatorPerEquipmentAdmin(admin.ModelAdmin):
    pass

@admin.register(AnalyzePerEquipment,site=custom_admin_site)
class AnalyzePerEquipmentAdmin(admin.ModelAdmin):
    pass

@admin.register(ExecutorPerAnalyze,site=custom_admin_site)
class ExecutorPerAnalyzeAdmin(admin.ModelAdmin):
    pass
