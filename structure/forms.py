from django import forms
import urllib

class SearchForm(forms.Form):
	q = forms.CharField(max_length=50)
	
	def get_list(self, structure_kind):
		# The search list is automatically everything
		out_list = [
			'name',
			'abbreviation',
		]
		if structure_kind == 'buildings':
			out_list.append('campus__name')
		if structure_kind == 'department':
			out_list.append('parent__name')
		return out_list
	
	def as_url_args(self):
		return urllib.urlencode(self.cleaned_data)