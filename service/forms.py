from django import forms
from django.contrib.localflavor.us import forms as lfus

from etcetera.structure import models as structure
from etcetera.service import models as service

SERVICE_CHOICES = (
	('repair','Problem'),
	('install','Install'),
)

class ServiceForm(forms.Form):
	name = forms.CharField(
		max_length=200,
		help_text='Your first and last name'
	)
	department = forms.CharField(
		max_length=100,
		help_text='Your university department'
	)
	phone = lfus.USPhoneNumberField(help_text='Format: ###-###-####')
	email = forms.EmailField(help_text='Your university email address')
	coordinator_check = forms.BooleanField(
		label='Have you consulted the classroom coordinator yet?',
		required=False,
		help_text='Check this only if you have already consulted \
			a classroom coordinator'
	)
	#building = forms.CharField(max_length=25)
	building = forms.ModelChoiceField(
		queryset=structure.Building.objects.all(),
		required=True,
		help_text='The university location of the request.'
	)
	room = forms.CharField(label="Room #", max_length=15)
	work_type = forms.ChoiceField(
		label='Request Type',
		choices=SERVICE_CHOICES,
		help_text='If new equipment is being installed, choose Install. \
			Otherwise, choose Problem'
	)
	equipment_text = forms.CharField(
		label='Equipment',
		max_length=75,
		required=False,
		help_text='The equipment in question, either a description or \
			make/model'
	)
	barcode = forms.CharField(
		label="Barcode?",
		max_length=6,
		required=False,
		help_text='If present, the number on the ETC barcode sticker'
	)
	description = forms.CharField(
		widget=forms.Textarea,
		help_text="Give a description of the request. If it's a repair, \
			what's broken, what are the symptoms? If it's an install, what \
			sort of equipment needs to be installed, and how? Be as specific \
			as possible so we can serve you best."
	)

class WorkOrderModelForm(forms.ModelForm):
	complete = forms.BooleanField(required=False)
	# I need to find a way to get the equipment object from the 'instance'
	# passed to this and make its barcode the default value for this field.
	barcode = forms.CharField(
		label="ETC Barcode",
		max_length=6,
		required=False,
	)
	
	class Meta:
		model = service.WorkOrder
		exclude = ('creation_date',)