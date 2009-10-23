import urllib

from django import forms
from django.contrib.localflavor.us import forms as lfus

from etcetera.structure import models as structure
from etcetera.checkout import models as checkout

class SearchForm(forms.Form):
	q = forms.CharField(max_length=50)
	name = forms.BooleanField(required=False, initial=True)
	department = forms.BooleanField(required=False, initial=True)
	equipment = forms.BooleanField(required=False, initial=True)
	location = forms.BooleanField(required=False, initial=True)
	
	def as_url_args(self):
		return urllib.urlencode(self.cleaned_data)
	
	def get_list(self):
		out_list = []
		data = self.cleaned_data
		if data['name']:
			out_list.extend(['first_name','last_name',])
		if data['department']:
			out_list.extend(['department__name','department_text',])
		if data['equipment']:
			out_list.append('equipment_needed',)
		if data['location']:
			out_list.extend(['building__name','room',])

class CheckoutModelForm(forms.ModelForm):
	class Meta:
		model = checkout.Checkout
		exclude = ('equipment_list','department_text','creation_date','creating_user',)

class AddEquipmentForm(forms.Form):
	barcode = forms.CharField(max_length=6, required=False)