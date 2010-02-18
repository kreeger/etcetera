from django import forms
from django.forms import ModelChoiceField

from etcetera.extras import models as extras

class UserModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj, *args, **kwargs):
		# Return a string of the format: "firstname lastname (username)"
		return "%s (%s)"%(obj.get_full_name(), obj.username)

class PasswordForm(forms.Form):
	password = forms.CharField(
		label='New password',
		widget=forms.PasswordInput,
	)
	password_check = forms.CharField(
		label='New password (again)',
		widget=forms.PasswordInput,
	)
	
	def clean(self):
		cd = self.cleaned_data
		if not cd['password'] == cd['password_check']:
			raise forms.ValidationError("The passwords do not match.")
		
		return cd

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = extras.UserProfile
		exclude = ('user',)