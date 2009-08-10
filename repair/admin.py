from etcetera.repair.models import WorkOrder
from django.contrib import admin

# This file determines what's shown in the admin interface
class WorkOrderAdmin(admin.ModelAdmin):
	raw_id_fields = ('equipment',)
<<<<<<< HEAD
	list_display = ('last_name','first_name','creation_date','priority','work_type','archived',)
	list_filter = ('work_type','priority','creation_date',)
=======
	list_display = ('last_name','first_name','creation_date','priority','work_type',)
	list_filter = ('building','work_type','priority',)
>>>>>>> e9f1e7a7f8a26d2ec46ccdbcc05b4efe9a7c227f
	search_fields = ('first_name','last_name','department','equipment__equipment_type__name','equipment_text','building__name','room','description','actions','technician__first_name','technician__last_name','technician__username','funding_source','work_type','budget',)

# Register the appropriate models 
admin.site.register(WorkOrder, WorkOrderAdmin)