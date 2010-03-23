from etcetera.service.models import WorkOrder
from django.contrib import admin

# This file determines what's shown in the admin interface
class WorkOrderAdmin(admin.ModelAdmin):
    raw_id_fields = ('equipment',)
    list_display = (
        'last_name',
        'first_name',
        'creation_date',
        'equipment_text',
        'priority',
        'work_type',
        'completion_date',
    )
    list_filter = (
        'work_type',
        'priority',
        'creation_date',
    )
    search_fields = (
        'first_name',
        'last_name',
        'department__name',
        'department_text',
        'equipment__equipment_type__name',
        'equipment_text','building__name',
        'room',
        'description',
        'actions',
        'technician__first_name',
        'technician__last_name',
        'technician__username',
        'funding_source',
        'work_type',
        'budget',
    )

# Register the appropriate models 
admin.site.register(WorkOrder, WorkOrderAdmin)