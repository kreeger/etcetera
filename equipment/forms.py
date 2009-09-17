import urllib

from django import forms

from etcetera.equipment import models as equipment

class EquipmentModelForm(forms.ModelForm):
	class Meta:
		model = equipment.Equipment
		exclude = ('custname',)

class EquipmentTypeModelForm(forms.ModelForm):
	class Meta:
		model = equipment.EquipmentType

class MakeModelForm(forms.ModelForm):
	class Meta:
		model = equipment.Make

class SearchForm(forms.Form):
	q = forms.CharField(max_length=50)
	equipment_type = forms.BooleanField(required=False, initial=True)
	barcode = forms.BooleanField(required=False, initial=True)
	location = forms.BooleanField(required=False, initial=True)
	serial = forms.BooleanField(required=False, initial=True)
	smsu_id = forms.BooleanField(required=False, initial=True)
	comments = forms.BooleanField(required=False, initial=True)
	
	def as_url_args(self):
		return urllib.urlencode(self.cleaned_data)
	
	def get_list(self):
		out_list = []
		data = self.cleaned_data
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