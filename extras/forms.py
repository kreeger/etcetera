from django import forms

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
