import urllib

from django import forms
from django.contrib.localflavor.us import forms as lfus
from django.contrib.auth import models as auth
from django.contrib.admin import widgets as adminwidgets

from etcetera.structure import models as structure
from etcetera.checkout import models as checkout
from etcetera.extras import forms as ef
from etcetera.extras.dateutil import formfield_callback, DateTimeField

class SearchForm(forms.Form):
    # The search query
    q = forms.CharField(max_length=50)
    # The special fields pertaining to model fields and such
    name = forms.BooleanField(required=False, initial=False)
    department = forms.BooleanField(required=False, initial=False)
    equipment = forms.BooleanField(required=False, initial=False)
    location = forms.BooleanField(required=False, initial=False)
    comments = forms.BooleanField(required=False, initial=False)
    
    def as_url_args(self):
        return urllib.urlencode(self.cleaned_data)
    
    def get_list(self):
        # The search list is automatically everything
        out_list = [
            'first_name',
            'last_name',
            'department__name',
            'department_text',
            'equipment_needed',
            'building__name',
            'room',
            'comments',
        ]
        data = self.cleaned_data
        # Unless one of the following is checked, then it's reset
        if data['name'] or data['department'] or data['equipment'] or data['location'] or data['comments']:
            out_list = []
        # And only the specified fields are added to it.
        if data['name']:
            out_list.extend(['first_name','last_name',])
        if data['department']:
            out_list.extend(['department__name','department_text',])
        if data['equipment']:
            out_list.append('equipment_needed',)
        if data['location']:
            out_list.extend(['building__name','room',])
        if data['comments']:
            out_list.append('comments',)
        # Return whatever it ends up being.
        return out_list

class CheckoutModelForm(forms.ModelForm):
    formfield_callback = formfield_callback
    class Meta:
        model = checkout.Checkout
        exclude = (
            'equipment_list',
            'department_text',
            'creation_date',
            'handling_user',
            'completion_date',
            'confirmation_sent',
            'action_date',
        )
    
    delivering_user = ef.UserModelChoiceField(
        auth.User.objects.all().order_by('last_name'),
        required=False,
    )

class CheckoutPublicForm(forms.ModelForm):
    formfield_callback = formfield_callback
    class Meta:
        model = checkout.Checkout
        exclude = (
            'equipment_list',
            'department',
            'handling_user',
            'creation_date',
            'delivering_user',
            'returning_user',
            'other_equipment',
            'comments',
            'completion_date',
            'confirmation_sent',
            'action_date',
            'canceled',
        )
    department_text = forms.CharField(
        max_length=100,
        help_text='The university department the request should be under.',
    )
    email = forms.EmailField(
        help_text="Your university email address.",
        required=True,
        max_length=75,
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

class DupeForm(forms.Form):
    out_date = DateTimeField()
    return_date = DateTimeField()

class CancelForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea
    )
