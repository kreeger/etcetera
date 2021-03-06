import urllib

from django import forms

from etcetera.reports import models as reports
from etcetera.extras.dateutil import formfield_callback, DateTimeField

class SearchForm(forms.Form):
    q = forms.CharField(max_length=50)
    
    def get_list(self):
        # The search list is automatically everything
        out_list = [
            'name',
        ]
        return out_list
    
    def as_url_args(self):
        return urllib.urlencode(self.cleaned_data)

class ReportModelForm(forms.ModelForm):
    formfield_callback = formfield_callback
    
    class Meta:
        model = reports.Report
        exclude = ('slug','created_by',)