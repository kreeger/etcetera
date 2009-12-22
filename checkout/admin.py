from etcetera.checkout.models import Checkout
from django.contrib import admin

# This file determines what's shown in the admin interface
class CheckoutAdmin(admin.ModelAdmin):
	fieldsets = (
		('Basic information', {
			'fields': (
				'first_name',
				'last_name',
				'department',
				'department_text',
				'course',
				'phone',
				'email',
				'building',
				'room',
				'creation_date',
				'handling_user',
			),
		}),
		('Checkout information', {
			'classes': (
				'collapse',
			),
			'fields': (
				'checkout_type',
				'return_type',
				'equipment_needed',
				'out_date',
				'return_date',
				'delivering_user',
				'returning_person',
				'equipment_list',
				'other_equipment',
				'completed',
			),
		}),
    )
	list_display = (
		'first_name',
		'last_name',
		'department',
		'equipment_needed',
		'checkout_type',
		'out_date',
	)
	list_filter = (
		'out_date',
	)
	search_fields = (
		'first_name',
		'last_name',
		'department__name',
		'department_text',
		'building__name',
		'room',
		'equipment_needed',
	)

# Register the appropriate models 
admin.site.register(Checkout, CheckoutAdmin)
