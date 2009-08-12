from etcetera.equipment.models import EquipmentType, Make, Equipment
from django.contrib import admin

# This file determines what's shown in the admin interface
class EquipmentAdmin(admin.ModelAdmin):
	fieldsets = (
		   ('Basic information', {
			  'fields': ('equipment_type', 'make', 'model', 'barcode', 'status', 'building', 'room', 'serial', 'last_inventoried', 'value','checkout_to',),
		   }),
		    ('Extra information', {
			  'classes': ('collapse',),
			  'fields': ('smsu_id', 'video_unit', 'property_control', 'lamp_type', 'on_weekly_checklist',),
		   }),
		   ('Purchase information', {
			  'classes': ('collapse',),
			  'fields': ('received_from', 'received_date', 'dof', 'purchase_order', 'budget',),
		   }),
			('Notes', {
				'fields': ('comments',),
			})
	    )
	list_display = ('equipment_type','barcode','make','model','status','building','room',)
	list_filter = ('status',)
	search_fields = ('equipment_type__name', 'building__name', 'room', 'make__name', 'model', 'barcode', 'serial', 'smsu_id', 'video_unit', 'lamp_type', 'received_from', 'dof', 'purchase_order', 'budget',)


# Register the appropriate models 
admin.site.register(EquipmentType)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Make)
