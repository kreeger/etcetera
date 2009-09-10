from django import forms
from etcetera.extras import models as extras

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
