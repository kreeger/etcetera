from etcetera.repair.models import WorkOrder
from django.contrib import admin

# This file determines what's shown in the admin interface
class WorkOrderAdmin(admin.ModelAdmin):
	raw_id_fields = ('equipment',)
	list_display = ('equipment','first_name','last_name','creation_date','priority','work_type',)
	list_filter = ('work_type',)
	search_fields = (
		'first_name',
		'last_name',
		'department',
		'equipment__equipment_type',
		'building__name',
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