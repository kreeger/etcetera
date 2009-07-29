from django import forms
from django.contrib.localflavor.us import forms as lfus
from etcetera.structure import models as structure

SERVICE_CHOICES = (
	('repair','Problem'),
	('install','Install'),
)

class ServiceForm(forms.Form):
	name = forms.CharField(max_length=200)
	department = forms.CharField(max_length=100)
	phone = lfus.USPhoneNumberField()
	email = forms.EmailField()
	# Have you worked with a classroom coordinator?
	#building = forms.CharField(max_length=25)
	building = forms.ModelChoiceField(queryset=structure.Building.objects.all(), required=True)
	room = forms.CharField(max_length=15)
	work_type = forms.ChoiceField(choices=SERVICE_CHOICES)
	equipment_text = forms.CharField(max_length=75, required=False)
	barcode = forms.CharField(max_length=6, required=False)
	description = forms.CharField(widget=forms.Textarea)