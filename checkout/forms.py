import urllib

from django import forms
from django.contrib.localflavor.us import forms as lfus
from django.contrib.auth import models as auth
from django.contrib.admin import widgets as adminwidgets

from etcetera.structure import models as structure
from etcetera.checkout import models as checkout
from etcetera.extras import forms as ef

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
		return out_list

class CheckoutModelForm(forms.ModelForm):
	class Meta:
		model = checkout.Checkout
		exclude = (
			'equipment_list',
			'department_text',
			'creation_date',
			'creating_user',
		)
	
	out_date = forms.DateTimeField(widget=adminwidgets.AdminSplitDateTime)
	return_date = forms.DateTimeField(widget=adminwidgets.AdminSplitDateTime)
	delivering_user = ef.UserModelChoiceField(
		auth.User.objects.all().order_by('last_name'),
		required=False,
	)

class CheckoutPublicForm(forms.ModelForm):
	class Meta:
		model = checkout.Checkout
		exclude = (
			'equipment_list',
			'department',
			'creating_user',
			'creating_date',
			'delivering_user',
			'completed',
			'returning_user',
			'other_equipment',
		)

class CheckoutEquipmentForm(forms.Form):
	barcodes = forms.CharField(
		max_length=255,
		required=False,
		help_text="Type in barcodes, separated by a space (i.e., \
			026629 027498 028380).",
	)
	video_unit = forms.IntegerField(
		required=False,
		help_text="If you'd like to add a video/TV cart, type in the \
			video cart's Unit #.",
	)
	cc_unit = forms.IntegerField(
		required=False,
		help_text="If you'd like to add a data projector/computer cart, type \
			in the computer cart's AV or Cart #.",
	)
