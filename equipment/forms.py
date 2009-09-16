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
