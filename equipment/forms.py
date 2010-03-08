import urllib

from django import forms
from django.contrib.auth import models as auth

from etcetera.equipment import models as equipment
from etcetera.extras.dateutil import formfield_callback, DateTimeField

class EquipmentModelForm(forms.ModelForm):
	formfield_callback = formfield_callback
	
	class Meta:
		model = equipment.Equipment
		exclude = ('custname','last_inventoried',)

class EquipmentTypeModelForm(forms.ModelForm):
	class Meta:
		model = equipment.EquipmentType
		exclude = ('slug',)

class MakeModelForm(forms.ModelForm):
	class Meta:
		model = equipment.Make
		exclude = ('slug',)

class SearchForm(forms.Form):
	q = forms.CharField(max_length=50)
	equipment_type = forms.BooleanField(required=False, initial=False)
	barcode = forms.BooleanField(required=False, initial=False)
	location = forms.BooleanField(required=False, initial=False)
	serial = forms.BooleanField(required=False, initial=False)
	smsu_id = forms.BooleanField(required=False, initial=False)
	comments = forms.BooleanField(required=False, initial=False)
	
	def as_url_args(self):
		return urllib.urlencode(self.cleaned_data)
	
	def get_list(self):
		# The search list is automatically everything
		out_list = [
			'equipment_type__name',
			'make__name',
			'model',
			'barcode',
			'building__name',
			'room',
			'serial',
			'smsu_id',
			'comments',
		]
		data = self.cleaned_data
		# Unless one of the following is checked, then it's reset
		if data['equipment_type'] or data['barcode'] or data['location'] or data['serial'] or data['smsu_id'] or data['comments']:
			out_list = []
		if data['equipment_type']:
			out_list.extend(['equipment_type__name','make__name','model',])
		if data['barcode']:
			out_list.append('barcode')
		if data['location']:
			out_list.extend(['building__name', 'room',])
		if data['serial']:
			out_list.append('serial')
		if data['smsu_id']:
			out_list.append('smsu_id')
		if data['comments']:
			out_list.append('comments')
		return out_list

class OtherSearchForm(forms.Form):
	q = forms.CharField(max_length=50)

	def as_url_args(self):
		return urllib.urlencode(self.cleaned_data)

	def get_list(self):
		# The search list is automatically everything
		out_list = [
			'name',
			'slug',
		]
		return out_list

class DupeForm(forms.Form):
	times = forms.IntegerField(
		label="How many copies would you like to make?",
		max_value=100
	)
